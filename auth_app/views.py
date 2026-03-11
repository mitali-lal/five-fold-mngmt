import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from .models import EmailVerification
from .email_service import send_verification_email

from users.models import FacultyProfile, StudentProfile
from activities_app.models import (
    Activity,
    ActivityRegistration,
    ActivityNotification,
    ResourceRequest
)

# ============================
# HELPERS
# ============================

def is_admin(user):
    return user.is_staff or user.is_superuser


# ============================
# AUTHENTICATION VIEWS
# ============================

def login_view(request):
    if request.method == "POST":
        role = request.POST.get("role")
        password = request.POST.get("password")

        if role == "admin":
            username = request.POST.get("username")

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is None or not user.is_superuser:
                return render(request, "auth_app/login.html", {
                    "error": "Invalid admin credentials"
                })

            login(request, user)
            return redirect("/admin-panel/dashboard/")

        else:
            email = request.POST.get("email")

            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, "auth_app/login.html", {
                    "error": "Invalid email or password"
                })

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user is None:
                return render(request, "auth_app/login.html", {
                    "error": "Invalid email or password"
                })

            # Email verification check
            verification = EmailVerification.objects.filter(user=user).first()
            if not verification or not verification.email_verified:
                return render(request, "auth_app/login.html", {
                    "error": "Please verify your email before logging in"
                })

            login(request, user)

            if role == "student":
                return redirect("/student/dashboard/")
            elif role == "faculty":
                return redirect("/faculty/dashboard/")

    return render(request, "auth_app/login.html")

@never_cache
def logout_view(request):
    logout(request)
    return redirect("/login/")


def signup_view(request):
    if request.method == "POST":
        role = request.POST.get("role")
        email = request.POST.get("email", "").lower()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # 1️⃣ Basic checks
        if password != confirm_password:
            return render(
                request,
                "auth_app/signup.html",
                {"error": "Passwords do not match"}
            )

        if not email.endswith("@banasthali.in"):
            return render(
                request,
                "auth_app/signup.html",
                {"error": "Only @banasthali.in emails are allowed"}
            )

        existing_user = User.objects.filter(email=email).first()

        # 2️⃣ Existing user logic
        if existing_user:
            if existing_user.is_active:
                return render(
                    request,
                    "auth_app/signup.html",
                    {"error": "An account with this email already exists"}
                )
            else:
                verification, _ = EmailVerification.objects.get_or_create(
                    user=existing_user
                )
                send_verification_email(existing_user, verification.token)
                return render(request, "auth_app/verify_notice.html")

        # 3️⃣ Generate readable username
        local_part = email.split("@")[0]
        if "_" in local_part:
            username = local_part.split("_", 1)[1]
        else:
            username = local_part

        # Ensure uniqueness
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # 4️⃣ Create user (inactive until verified)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = False
        user.save()

        # 5️⃣ Send verification email
        verification = EmailVerification.objects.create(user=user)
        send_verification_email(user, verification.token)

        return render(request, "auth_app/verify_notice.html")

    return render(request, "auth_app/signup.html")

# ============================
# DASHBOARDS
# ============================

@login_required
def student_dashboard(request):
    registrations = ActivityRegistration.objects.filter(
        student=request.user
    ).select_related("activity")

    notifications = ActivityNotification.objects.filter(
        activity__in=registrations.values_list("activity", flat=True),
        status="sent",
        send_in_app=True
    ).order_by("-created_at")[:10]

    # 🔥 ADD THIS BLOCK
    try:
        profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        profile = None

    return render(
        request,
        "student/dashboard.html",
        {
            "registrations": registrations,
            "notifications": notifications,
            "profile": profile,  # 🔥 THIS WAS MISSING
        }
    )


@login_required
def faculty_dashboard(request):
    activities = Activity.objects.filter(faculty=request.user)

    resource_requests = ResourceRequest.objects.filter(
        sender=request.user
    ).select_related("activity")

    return render(
        request,
        "faculty/dashboard.html",
        {
            "activities": activities,
            "resource_requests": resource_requests,
        }
    )


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(
        request,
        "admin/dashboard.html",
        {
            "total_students": StudentProfile.objects.count(),
            "total_faculty": FacultyProfile.objects.count(),
            "total_activities": Activity.objects.count(),
            "total_registrations": ActivityRegistration.objects.count(),
            "pending_resource_requests": ResourceRequest.objects.filter(
                status="pending"
            ).count(),
        }
    )


# ============================
# MISC
# ============================

@login_required
def student_settings(request):
    return render(request, "student/settings.html")


@login_required
def student_feedback(request):
    return render(request, "student/feedback.html")


@login_required
def campus_map(request):
    return render(request, "student/campus_map.html")


def verify_email(request, token):
    try:
        record = EmailVerification.objects.get(token=token)
        record.email_verified = True
        record.save()

        user = record.user
        user.is_active = True   # 🔓 ACTIVATE ACCOUNT
        user.save()

        return redirect("/login/?verified=1")

    except EmailVerification.DoesNotExist:
        return redirect("/login/?error=invalid_link")
