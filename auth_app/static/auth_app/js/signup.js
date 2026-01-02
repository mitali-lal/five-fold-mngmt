document.getElementById("signupForm").addEventListener("submit", function (e) {
    e.preventDefault();

    let role = document.getElementById("role").value;
    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirmPassword").value;

    let valid = true;

    // Clear errors
    document.getElementById("roleError").textContent = "";
    document.getElementById("nameError").textContent = "";
    document.getElementById("emailError").textContent = "";
    document.getElementById("passwordError").textContent = "";
    document.getElementById("confirmPasswordError").textContent = "";

    if (role === "") {
        document.getElementById("roleError").textContent = "Role is required";
        valid = false;
    }

    if (name === "") {
        document.getElementById("nameError").textContent = "Name is required";
        valid = false;
    }

    if (email === "") {
        document.getElementById("emailError").textContent = "Email is required";
        valid = false;
    } else if (!email.endsWith("@banasthali.in")) {
        document.getElementById("emailError").textContent =
            "Email must end with @banasthali.in";
        valid = false;
    }

    if (password === "") {
        document.getElementById("passwordError").textContent =
            "Password is required";
        valid = false;
    }

    if (confirmPassword === "") {
        document.getElementById("confirmPasswordError").textContent =
            "Please confirm password";
        valid = false;
    } else if (password !== confirmPassword) {
        document.getElementById("confirmPasswordError").textContent =
            "Passwords do not match";
        valid = false;
    }

    if (valid) {
        // TODO (backend): create user using Django auth APIs
        window.location.href = "/login/";
    }
});
