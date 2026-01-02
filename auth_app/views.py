from django.shortcuts import render

def login_view(request):
    return render(request, "auth_app/login.html")
def student_dashboard(request):
    return render(request, "student/dashboard.html")

def faculty_dashboard(request):
    return render(request, "faculty/dashboard.html")

def admin_dashboard(request):
    return render(request, "admin/dashboard.html")
def signup_view(request):
    return render(request, "auth_app/signup.html")
