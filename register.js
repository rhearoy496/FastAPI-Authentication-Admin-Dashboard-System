document.getElementById("registerForm")?.addEventListener("submit", async function(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("name", document.getElementById("reg_name").value);
    formData.append("email", document.getElementById("reg_email").value);
    formData.append("password", document.getElementById("reg_password").value);
    formData.append("profile_image", document.getElementById("reg_image").files[0]);

    const response = await fetch("/register", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    if (response.ok) {
        alert("Registration successful. Please login.");
        window.location.href = "/";
    } else {
        document.getElementById("reg_message").innerText = data.detail;
    }
});