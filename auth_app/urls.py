from django.urls import path
from .views import (
    login_view,
    logout_view,
    student_dashboard,
    faculty_dashboard,
    admin_dashboard,
    signup_view,
    verify_email,
)
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("student/dashboard/", student_dashboard, name="student_dashboard"),
    path("faculty/dashboard/", faculty_dashboard, name="faculty_dashboard"),
    path("admin-panel/dashboard/", admin_dashboard, name="admin_dashboard"),

    path("signup/", signup_view, name="signup"),
    path(
    "users/settings/",
    views.student_settings,
    name="student_settings"
),
path(
    "campus/map/",
    views.campus_map,
    name="campus_map"
),
path(
    "feedback/student/",
    views.student_feedback,
    name="student_feedback"
),
path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="auth_app/forgot_password.html"
        ),
        name="password_reset",
    ),
    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth_app/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth_app/reset_password.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth_app/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),


]
