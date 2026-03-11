# ======================
# IMPORTS
# ======================
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils.timezone import now

from .models import (
    Activity,
    ActivityRegistration,
    ActivityMedia,
    Feedback,
    ResourceRequest,
    Attendance,
)

from users.models import StudentProfile


# ======================
# PERMISSION CHECK
# ======================
def is_admin(user):
    return user.is_staff or user.is_superuser


# ==========================================================
# ====================== ACTIVITIES ========================
# ==========================================================
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, "admin/dashboard.html")


@login_required
@user_passes_test(is_admin)
def manage_activities(request):
    activities = Activity.objects.select_related("faculty").order_by("-id")
    return render(
        request,
        "activities_app/admin/manage_activities.html",
        {"activities": activities},
    )


@login_required
@user_passes_test(is_admin)
def create_activity(request):
    return render(
        request,
        "activities_app/admin/create_activity.html"
    )


@login_required
@user_passes_test(is_admin)
def admin_edit_activity(request, id):
    activity = get_object_or_404(Activity, id=id)

    students = ActivityRegistration.objects.filter(
        activity=activity
    ).select_related("student")

    media_files = ActivityMedia.objects.filter(activity=activity)
    faculty_list = User.objects.filter(is_staff=True)

    if request.method == "POST":
        activity.title = request.POST.get("title")
        activity.description = request.POST.get("description")
        activity.schedule = request.POST.get("schedule")
        activity.requirements = request.POST.get("requirements")
        activity.quick_notes = request.POST.get("quick_notes")
        activity.fee = request.POST.get("fee") or 0

        faculty_id = request.POST.get("faculty")
        activity.faculty_id = faculty_id if faculty_id else None

        activity.save()
        return redirect("admin_manage_activities")

    return render(
        request,
        "activities_app/admin/activity_edit.html",
        {
            "activity": activity,
            "students": students,
            "media_files": media_files,
            "faculty_list": faculty_list,
        },
    )


@login_required
@user_passes_test(is_admin)
def admin_delete_activity(request, id):
    activity = get_object_or_404(Activity, id=id)
    activity.delete()
    return redirect("admin_manage_activities")


@require_POST
@login_required
@user_passes_test(is_admin)
def admin_bulk_action(request):
    action = request.POST.get("action")
    ids = request.POST.getlist("activity_ids")

    if not ids:
        return redirect("admin_manage_activities")

    qs = Activity.objects.filter(id__in=ids)

    if action == "enable":
        qs.update(is_active=True)
    elif action == "disable":
        qs.update(is_active=False)
    elif action == "delete":
        qs.delete()

    return redirect("admin_manage_activities")


@login_required
@user_passes_test(is_admin)
def admin_activity_feedback(request, id):
    activity = get_object_or_404(Activity, id=id)
    feedbacks = Feedback.objects.filter(activity=activity).order_by("-created_at")

    return render(
        request,
        "activities_app/faculty/faculty_feedback.html",
        {
            "activity": activity,
            "feedbacks": feedbacks,
            "is_admin": True,
        },
    )


# ==========================================================
# =================== RESOURCE REQUESTS ====================
# ==========================================================

@login_required
@user_passes_test(is_admin)
def admin_resource_requests(request):
    requests = ResourceRequest.objects.select_related(
        "activity", "sender"
    ).order_by("-created_at")

    return render(
        request,
        "activities_app/admin/resource_requests.html",
        {"requests": requests},
    )


@login_required
@user_passes_test(is_admin)
def update_resource_request(request, id):
    resource_request = get_object_or_404(ResourceRequest, id=id)

    if request.method == "POST":
        resource_request.status = request.POST.get("status")
        resource_request.admin_remarks = request.POST.get("admin_remarks", "")
        resource_request.save()

    return redirect("admin_resource_requests")


# ==========================================================
# ===================== STUDENTS LIST ======================
# ==========================================================

@login_required
@user_passes_test(is_admin)
def admin_students_list(request):
    students_qs = User.objects.filter(
        student_profile__isnull=False
    ).select_related("student_profile")

    # -------- SEARCH --------
    q = request.GET.get("q")
    if q:
        students_qs = students_qs.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )

    # -------- FILTERS --------
    hostel = request.GET.get("hostel")
    if hostel:
        students_qs = students_qs.filter(student_profile__hostel=hostel)

    course = request.GET.get("course")
    if course:
        students_qs = students_qs.filter(student_profile__course=course)

    year = request.GET.get("year")
    if year:
        students_qs = students_qs.filter(student_profile__year=year)

    status = request.GET.get("status")
    if status == "active":
        students_qs = students_qs.filter(is_active=True)
    elif status == "inactive":
        students_qs = students_qs.filter(is_active=False)

    fold = request.GET.get("fold")
    if fold:
        students_qs = students_qs.filter(
            activityregistration__activity__fold=fold
        ).distinct()

    # -------- ANNOTATIONS --------
    students_qs = students_qs.annotate(
        activity_count=Count("activityregistration", distinct=True)
    ).order_by("username")

    # -------- PAGINATION --------
    paginator = Paginator(students_qs, 50)
    page_obj = paginator.get_page(request.GET.get("page"))

    # -------- STATS --------
    total_students = students_qs.count()
    active_students = students_qs.filter(is_active=True).count()
    new_this_month = students_qs.filter(
        date_joined__month=now().month,
        date_joined__year=now().year
    ).count()

    return render(
        request,
        "activities_app/admin/students_list.html",
        {
            "page_obj": page_obj,
            "total_students": total_students,
            "active_students": active_students,
            "new_this_month": new_this_month,
            "filters": request.GET,
        }
    )


# ==========================================================
# ==================== STUDENT DETAIL ======================
# ==========================================================

@login_required
@user_passes_test(is_admin)
def admin_student_detail(request, id):
    student = get_object_or_404(
        User.objects.select_related("student_profile"),
        id=id,
        student_profile__isnull=False
    )

    profile = student.student_profile

    registrations = (
        ActivityRegistration.objects
        .filter(student=student)
        .select_related("activity")
    )

    attendance_stats = (
        Attendance.objects
        .filter(student=student)
        .values("activity__title")
        .annotate(
            total=Count("id"),
            present=Count("id", filter=Q(status="Present"))
        )
    )

    return render(
        request,
        "activities_app/admin/student_detail.html",
        {
            "student": student,
            "profile": profile,
            "registrations": registrations,
            "attendance_stats": attendance_stats,
        }
    )


# ==========================================================
# ===================== STUDENT EDIT =======================
# ==========================================================

@login_required
@user_passes_test(is_admin)
def admin_student_edit(request, id):
    student = get_object_or_404(
        User,
        id=id,
        student_profile__isnull=False
    )
    profile = student.student_profile

    if request.method == "POST":
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.email = request.POST.get("email")

        profile.course = request.POST.get("course")
        profile.year = request.POST.get("year")
        profile.hostel = request.POST.get("hostel")
        profile.fold = request.POST.get("fold")

        student.save()
        profile.save()

        return redirect("admin_student_detail", id=student.id)

    return render(
        request,
        "activities_app/admin/student_edit.html",
        {"student": student, "profile": profile},
    )


# ==========================================================
# =================== STUDENT DEACTIVATE ===================
# ==========================================================

@require_POST
@login_required
@user_passes_test(is_admin)
def admin_student_deactivate(request, id):
    student = get_object_or_404(
        User,
        id=id,
        student_profile__isnull=False
    )
    student.is_active = False
    student.save()
    return redirect("admin_students_list")

from users.models import StudentProfile
from django.contrib import messages

@login_required
@user_passes_test(is_admin)
def admin_student_add(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        course = request.POST.get("course")
        year = request.POST.get("year")
        hostel = request.POST.get("hostel")
        fold = request.POST.get("fold")

        # -------- BASIC VALIDATION --------
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("admin_student_add")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("admin_student_add")

        # -------- CREATE USER --------
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
        )

        # -------- CREATE STUDENT PROFILE --------
        StudentProfile.objects.create(
            user=user,
            course=course,
            year=year,
            hostel=hostel,
            fold=fold,
        )

        messages.success(request, "Student added successfully")
        return redirect("admin_students_list")

    return render(
        request,
        "activities_app/admin/student_add.html"
    )

from django.db.models import Q, Count
from django.utils.timezone import now

@login_required
@user_passes_test(is_admin)
def admin_students_export_pdf(request):
    students = User.objects.filter(
        student_profile__isnull=False
    ).select_related("student_profile")

    # -------- APPLY SAME FILTERS --------
    q = request.GET.get("q")
    if q:
        students = students.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )

    hostel = request.GET.get("hostel")
    if hostel:
        students = students.filter(student_profile__hostel=hostel)

    course = request.GET.get("course")
    if course:
        students = students.filter(student_profile__course=course)

    status = request.GET.get("status")
    if status == "active":
        students = students.filter(is_active=True)
    elif status == "inactive":
        students = students.filter(is_active=False)

    students = students.annotate(
        activity_count=Count("activityregistration", distinct=True)
    ).order_by("username")

    return render(
        request,
        "activities_app/admin/students_export_pdf.html",
        {
            "students": students,
            "generated_on": now(),
        }
    )

from django.db.models import Count
from activities_app.models import FacultyTimeSlot

@login_required
@user_passes_test(is_admin)
def admin_faculty_list(request):
    faculty_qs = (
        User.objects
        .filter(is_staff=True)
        .exclude(is_superuser=True)
        .annotate(
            activity_count=Count("activities", distinct=True),
            slot_count=Count("time_slots", distinct=True),
        )
        .order_by("username")
    )

    return render(
        request,
        "activities_app/admin/faculty_list.html",
        {
            "faculty_list": faculty_qs,
            "total_faculty": faculty_qs.count(),
        }
    )

@login_required
@user_passes_test(is_admin)
def admin_faculty_detail(request, id):
    faculty = get_object_or_404(User, id=id, is_staff=True)

    activities = Activity.objects.filter(faculty=faculty)

    slots = FacultyTimeSlot.objects.filter(faculty=faculty)

    return render(
        request,
        "activities_app/admin/faculty_detail.html",
        {
            "faculty": faculty,
            "activities": activities,
            "slots": slots,
        }
    )

from datetime import time

@login_required
@user_passes_test(is_admin)
def admin_faculty_assign(request, id):
    faculty = get_object_or_404(User, id=id, is_staff=True)
    activities = Activity.objects.all()

    if request.method == "POST":
        activity_id = request.POST.get("activity")
        day = request.POST.get("day")
        start = request.POST.get("start_time")
        end = request.POST.get("end_time")

        # Assign activity
        activity = get_object_or_404(Activity, id=activity_id)
        activity.faculty = faculty
        activity.save()

        # Create slot
        FacultyTimeSlot.objects.create(
            faculty=faculty,
            day=day,
            start_time=start,
            end_time=end,
        )

        return redirect("admin_faculty_detail", id=faculty.id)

    return render(
        request,
        "activities_app/admin/faculty_assign.html",
        {
            "faculty": faculty,
            "activities": activities,
        }
    )

from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.core.paginator import Paginator

@login_required
@user_passes_test(is_admin)
def admin_faculty_hub(request):
    view = request.GET.get("view", "home")
    faculty_id = request.GET.get("id")
    selected_faculty_id = request.GET.get("faculty")  # For assign view

    # Get all faculty (users with faculty_profile)
    faculty_qs = User.objects.filter(
        faculty_profile__isnull=False
    ).select_related("faculty_profile")

    # 🔍 SEARCH
    q = request.GET.get("q")
    if q:
        faculty_qs = faculty_qs.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )

    faculty_qs = faculty_qs.annotate(
        activity_count=Count("activities", distinct=True)
    ).order_by("username")

    # 📄 PAGINATION
    paginator = Paginator(faculty_qs, 25)
    page_obj = paginator.get_page(request.GET.get("page"))

    # 👁️ VIEW DETAIL
    faculty_detail = None
    if view == "detail" and faculty_id:
        faculty_detail = get_object_or_404(
            User.objects.select_related("faculty_profile"),
            id=faculty_id,
            faculty_profile__isnull=False
        )

    # GET ACTIVITIES FOR ASSIGN VIEW - Use all activities since there's no is_active field
    activities = Activity.objects.all().order_by('title')
    
    # GET TIME SLOTS FOR ASSIGN VIEW - Check if FacultyTimeSlot model exists
    # If not, use a default or check your actual model name
    try:
        from activities_app.models import FacultyTimeSlot
        time_slots = FacultyTimeSlot.objects.all().order_by('day', 'start_time')
    except:
        # If FacultyTimeSlot doesn't exist, create empty queryset
        time_slots = []

    # GET ALL FACULTY FOR DROPDOWN
    all_faculty = User.objects.filter(
        faculty_profile__isnull=False
    ).order_by('username')

    context = {
        "current_view": view,
        "page_obj": page_obj,
        "faculty_detail": faculty_detail,
        "filters": request.GET,
        "activities": activities,
        "time_slots": time_slots,
        "all_faculty": all_faculty,
        "selected_faculty_id": selected_faculty_id,
    }

    return render(
        request,
        "activities_app/admin/faculty_hub.html",
        context
    )
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse

@login_required
@user_passes_test(is_admin)
def admin_faculty_export_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="faculty_list.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    y = 800

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Faculty List")
    y -= 30

    p.setFont("Helvetica", 10)

    for faculty in User.objects.filter(faculty_profile__isnull=False):
        line = f"{faculty.get_full_name()} | {faculty.email}"
        p.drawString(50, y, line)
        y -= 18
        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response

@login_required
@user_passes_test(is_admin)
def admin_faculty_deactivate(request, id):
    faculty = get_object_or_404(
        User,
        id=id,
        faculty_profile__isnull=False
    )

    faculty.is_active = False
    faculty.save()

    return redirect("admin_faculty_hub")

import json
from django.utils import timezone

@login_required
@user_passes_test(is_admin)
def admin_faculty_assign(request):
    if request.method == "POST":
        try:
            faculty_id = request.POST.get("faculty_id")
            activity_id = request.POST.get("activity_id")
            time_slots_data = request.POST.get("time_slots")
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            
            faculty = get_object_or_404(User, id=faculty_id)
            activity = get_object_or_404(Activity, id=activity_id)
            
            # Update activity with faculty
            activity.faculty = faculty
            
            # Parse time slots data
            time_slots = json.loads(time_slots_data) if time_slots_data else []
            
            # Create schedule string from selected slots
            if time_slots:
                schedule_parts = []
                # Group by day
                days_dict = {}
                for slot in time_slots:
                    day = slot.get('day')
                    time = slot.get('time')
                    period = slot.get('period')
                    
                    if day not in days_dict:
                        days_dict[day] = []
                    days_dict[day].append(f"{time} ({period})")
                
                # Build schedule string
                for day, times in days_dict.items():
                    schedule_parts.append(f"{day}: {', '.join(times)}")
                
                schedule = "; ".join(schedule_parts)
                
                # Add date range
                if start_date:
                    schedule += f" | From: {start_date}"
                    if end_date:
                        schedule += f" to {end_date}"
                
                activity.schedule = schedule
            
            activity.save()
            
            # Redirect back with success message
            return redirect("/admin-panel/faculty/?view=list&message=Faculty assigned successfully!&status=success")
            
        except Exception as e:
            # Redirect back with error message
            return redirect(f"/admin-panel/faculty/?view=assign&message=Error: {str(e)}&status=error")
    
    # If not POST, redirect to assign page
    return redirect("/admin-panel/faculty/?view=assign")

def admin_notifications(request):
    return render(request, "activities_app/admin/admin_notification_hub.html")

from django.shortcuts import render

def audit_logs(request):
    return render(request, "activities_app/admin/audit_logs.html")

def system_settings(request):
    return render(request, "activities_app/admin/system_settings.html")
