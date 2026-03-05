from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import models
from database import engine
from models import Base
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas
from auth import hash_password, verify_password, create_access_token
from auth import get_current_user
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import File, UploadFile, Form
import shutil
import uuid

Base.metadata.create_all(bind=engine)



app = FastAPI()
# app = FastAPI(docs_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# @app.get("/")
# def root():
#     return {"message": "Server is running"}

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register-page", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard-page", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.post("/register")
# def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     existing = db.query(models.User).filter(models.User.email == user.email).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     new_user = models.User(
#         email=user.email,
#         hashed_password=hash_password(user.password)
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message": "User created successfully"}

@app.post("/register")
async def register(
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    profile_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Save image
    filename = f"{uuid.uuid4()}_{profile_image.filename}"
    file_path = f"uploads/{filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(profile_image.file, buffer)

    new_user = models.User(
        email=email,
        name=name,
        profile_image=filename,
        hashed_password=hash_password(password),
        is_admin=False
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}


# @app.post("/login")
# def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.email == user.email).first()

#     if not db_user:
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     if not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     token = create_access_token({"sub": str(db_user.id)})

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }



@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(db_user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/me")
def read_users_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

@app.get("/dashboard")
def dashboard(current_user = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email,
        "profile_image": current_user.profile_image,
        "is_admin": current_user.is_admin
    }

@app.get("/admin-data")
def admin_data(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    users = db.query(models.User).all()

    return {
        "total_users": len(users),
        "users": [
            {
                "email": user.email,
                "name": user.name,
                "profile_image": user.profile_image
            }
            for user in users
        ]
    }

@app.get("/admin-page", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/all-users")
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users