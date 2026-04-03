import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from .models import EmailVerification
from .email_service import send_verification_email

from .models import Feedback
from django.contrib import messages

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
@never_cache
def student_dashboard(request):
    registrations = ActivityRegistration.objects.filter(
        student=request.user
    ).select_related("activity")

    notifications = ActivityNotification.objects.filter(
        activity__in=registrations.values_list("activity", flat=True),
        status="sent",
        send_in_app=True
    ).order_by("-created_at")[:10]

    try:
        profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        profile = None

    response = render(
        request,
        "student/dashboard.html",
        {
            "registrations": registrations,
            "notifications": notifications,
            "profile": profile,
        }
    )

    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response

@login_required
@never_cache
def faculty_dashboard(request):
    activities = Activity.objects.filter(faculty=request.user)

    resource_requests = ResourceRequest.objects.filter(
        sender=request.user
    ).select_related("activity")

    response = render(
        request,
        "faculty/dashboard.html",
        {
            "activities": activities,
            "resource_requests": resource_requests,
        }
    )

    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response



@login_required
@never_cache
@user_passes_test(is_admin)
def admin_dashboard(request):
    response = render(
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

    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response


# ============================
# MISC
# ============================

@login_required
def student_settings(request):
    return render(request, "student/settings.html")


@login_required
def student_feedback(request):

    if request.method == "POST":
        Feedback.objects.create(
            user=request.user,
            category=request.POST.get('category'),
            module=request.POST.get('module'),
            issue_type=request.POST.get('issue_type'),
            description=request.POST.get('description'),
            expected=request.POST.get('expected'),
            priority=request.POST.get('priority'),
            affected_users=request.POST.get('affected_users'),
            followup_preference=request.POST.get('followup_preference'),
            additional_comments=request.POST.get('additional_comments'),
            attachment=request.FILES.get('attachment'),
        )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('student_feedback')   # ✅ IMPORTANT

    # ✅ ALWAYS define this
    user_feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "student/feedback.html", {
        "feedbacks": user_feedbacks
    })

@login_required
def campus_map(request):
    activities = Activity.objects.all()   # 👈 ADD THIS

    return render(
        request,
        "student/campus_map.html",
        {
            "activities": activities   # 👈 ADD THIS
        }
    )


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
