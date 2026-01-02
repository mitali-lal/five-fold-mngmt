document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();

    let role = document.getElementById("role").value;
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value;

    let valid = true;

    // Clear errors
    document.getElementById("roleError").textContent = "";
    document.getElementById("emailError").textContent = "";
    document.getElementById("passwordError").textContent = "";

    if (role === "") {
        document.getElementById("roleError").textContent = "Role is required";
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

    if (valid) {
        // Later this will call backend
        //console.log("Login validated");
        const role = document.getElementById("role").value;

    if (role === "STUDENT") {
        window.location.href = "/student/dashboard/";
    } 
    else if (role === "FACULTY") {
        window.location.href = "/faculty/dashboard/";
    } 
    else if (role === "ADMIN") {
        window.location.href = "/admin/dashboard/";
    }
    }
});
