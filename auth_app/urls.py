from django.urls import path
from .views import (
    login_view,
    student_dashboard,
    faculty_dashboard,
    admin_dashboard,
    signup_view
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("student/dashboard/", student_dashboard),
    path("faculty/dashboard/", faculty_dashboard),
    path("admin/dashboard/", admin_dashboard),
    path("signup/", signup_view, name="signup"),

]
