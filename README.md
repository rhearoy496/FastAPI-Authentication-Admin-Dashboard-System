# FastAPI Authentication & Admin Dashboard System

A full-stack authentication system built with FastAPI and JWT authentication.

## Features

- User registration with profile image upload
- Secure login with bcrypt password hashing
- JWT-based authentication
- Role-based access control (Admin/User)
- User dashboard with profile display
- Admin dashboard to view registered users
- REST API backend with FastAPI
- HTML/CSS/JavaScript frontend integration

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- HTML, CSS, JavaScript

## System Architecture 

  Frontend (HTML, CSS, JavaScript)
        ↓
  FastAPI Backend (REST API)
        ↓
  JWT Authentication
        ↓
  SQLite Database


## Screenshots
  Registration :
    <img width="1919" height="882" alt="image" src="https://github.com/user-attachments/assets/cec4df51-4020-4e1d-9ee6-47261880832f" />
  Login :
    <img width="1900" height="906" alt="image" src="https://github.com/user-attachments/assets/1d57d408-6e18-4344-8a41-494f2e78e5ae" />
  Admin Dashboard :
    <img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/c0e3b748-4794-4f5c-91ad-1e3be1a9fe3c" />
  User Dashboard :
    <img width="1914" height="913" alt="image" src="https://github.com/user-attachments/assets/de739186-d5d1-4c69-b2eb-3d5142b8fc4c" />


## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/fastapi-auth-admin-dashboard.git

Install dependencies:

pip install -r requirements.txt

Run the server:

uvicorn main:app --reload

Open in browser:

http://127.0.0.1:8000
