from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from users.models import StudentProfile
from datetime import datetime, timedelta
import random

from .models import (
    Activity,
    ActivityRegistration,
    Attendance,
    ActivityMedia,
    ActivityNotification,
    ResourceRequest
)

# =====================================================
# NOTE:
# User Management module is not implemented yet.
# User.username is used as temporary student identifier.
# Attendance percentages are frontend-fake.
# ERP/UserProfile integration will replace this later.
# =====================================================


# ======================
# STUDENT VIEWS
# ======================

from .models import Feedback

@login_required
@require_POST
def submit_feedback(request, id):
    activity = get_object_or_404(Activity, id=id)

    # Ensure only registered students can give feedback
    if not ActivityRegistration.objects.filter(
        student=request.user,
        activity=activity
    ).exists():
        return redirect("activity_detail", id=id)

    Feedback.objects.create(
        activity=activity,
        rating=int(request.POST.get("rating")),
        comment=request.POST.get("comment")
    )

    messages.success(request, "Feedback submitted successfully.")
    return redirect("activity_detail", id=id)


def browse_activities(request):
    activities = Activity.objects.all()

    registered_activity_ids = []
    if request.user.is_authenticated:
        registered_activity_ids = ActivityRegistration.objects.filter(
            student=request.user
        ).values_list("activity_id", flat=True)

    return render(
        request,
        "activities_app/student/browse_activities.html",
        {
            "activities": activities,
            "registered_activity_ids": registered_activity_ids
        }
    )


def activity_detail(request, id):
    activity = get_object_or_404(Activity, id=id)

    available_seats = activity.total_seats - activity.filled_seats

    is_registered = False
    if request.user.is_authenticated:
        is_registered = ActivityRegistration.objects.filter(
            student=request.user,
            activity=activity
        ).exists()

    related_activities = Activity.objects.filter(
        fold=activity.fold
    ).exclude(id=activity.id)[:3]

    feedbacks = activity.feedbacks.all()

    # 🔥 BACK URL LOGIC
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        back_url = "/admin-panel/activities/manage/"
    else:
        back_url = "/activities/student/activities/"

    return render(
        request,
        "activities_app/student/activity_detail.html",
        {
            "activity": activity,
            "available_seats": available_seats,
            "related_activities": related_activities,
            "feedbacks": feedbacks,
            "is_registered": is_registered,
            "back_url": back_url,   # ✅ PASS THIS
        }
    )



@login_required
def my_registrations(request):
    registrations = ActivityRegistration.objects.filter(student=request.user)
    return render(
        request,
        "activities_app/student/my_registrations.html",
        {"registrations": registrations}
    )


@login_required
def register_activity(request, id):
    if request.method != "POST":
        return redirect("activity_detail", id=id)

    from django.urls import reverse

    try:
        profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.error(
            request,
            "Please complete your profile before registering for an activity."
        )
        return redirect(
            f"{reverse('student_profile')}?next={request.path}"
        )

    # ✅ CORRECT FIELD (EXISTING IN DB)
    if not profile.is_profile_complete:
        messages.error(
            request,
            "Please complete your profile before registering for an activity."
        )
        return redirect(
            f"{reverse('student_profile')}?next={request.path}"
        )

    activity = get_object_or_404(Activity, id=id)

    ActivityRegistration.objects.get_or_create(
        student=request.user,
        activity=activity
    )

    messages.success(request, "Successfully registered for the activity.")
    return redirect("activity_detail", id=id)


@login_required
def attendance_overview(request, id):
    activity = get_object_or_404(Activity, id=id)

    records = Attendance.objects.filter(
        activity=activity,
        student=request.user
    ).order_by("date")

    if not records.exists():
        fake_records = generate_fake_attendance(activity, request.user)
        present = sum(1 for r in fake_records if r["status"] == "Present")
        absent = sum(1 for r in fake_records if r["status"] == "Absent")
        attendance_records_list = fake_records
    else:
        present = records.filter(status="Present").count()
        absent = records.filter(status="Absent").count()
        attendance_records_list = [
            {"date": r.date, "status": r.status} for r in records
        ]

    total = present + absent
    percent = int((present / total) * 100) if total else 0

    return render(
        request,
        "activities_app/student/attendance_panel.html",
        {
            "activity": activity,
            "attendance_records": attendance_records_list,
            "present": present,
            "absent": absent,
            "total_sessions": total,
            "percent": percent
        }
    )


@login_required
def student_notifications(request):
    registered_activities = ActivityRegistration.objects.filter(
        student=request.user
    ).values_list("activity_id", flat=True)

    notifications = ActivityNotification.objects.filter(
        activity_id__in=registered_activities,
        status="sent"
    ).order_by("-created_at")

    return render(
        request,
        "activities_app/student/notifications.html",
        {
            "notifications": notifications
        }
    )


# ======================
# FACULTY VIEWS
# ======================




@login_required
def assigned_activities(request):
    activities = Activity.objects.filter(faculty=request.user)
    return render(
        request,
        "activities_app/faculty/assigned_activities.html",
        {"activities": activities}
    )


@login_required
def activity_workspace(request, id):
    activity = get_object_or_404(
        Activity,
        id=id,
        faculty=request.user
    )

    students = ActivityRegistration.objects.filter(
        activity=activity
    ).select_related("student")

    media_files = ActivityMedia.objects.filter(activity=activity)

    return render(
        request,
        "activities_app/faculty/activity_workspace.html",
        {
            "activity": activity,
            "students": students,
            "media_files": media_files
        }
    )


@login_required
def faculty_attendance(request, id):
    activity = get_object_or_404(Activity, id=id, faculty=request.user)

    registrations = ActivityRegistration.objects.filter(
        activity=activity
    ).select_related("student")

    students = []
    for reg in registrations:
        user = reg.student
        students.append({
            "name": user.get_full_name() or user.username,
            "roll_no": user.username,  # TEMP placeholder
            "email": user.email,
            "attendance": random.randint(70, 95),  # FAKE
        })

    total = len(students)
    present_today = int(total * 0.85)

    return render(
        request,
        "activities_app/faculty/faculty_attendance.html",
        {
            "activity": activity,
            "students": students,
            "present_today": present_today,
            "absent_today": total - present_today,
        }
    )


@require_POST
@login_required
def update_activity(request, id):
    activity = get_object_or_404(
        Activity,
        id=id,
        faculty=request.user
    )

    activity.description = request.POST.get("description")
    activity.schedule = request.POST.get("schedule")
    activity.requirements = request.POST.get("requirements")
    activity.quick_notes = request.POST.get("quick_notes")
    activity.save()

    messages.success(request, "Activity updated successfully")
    return redirect("activity_workspace", id=activity.id)


@require_POST
@login_required
def add_media(request, id):
    activity = get_object_or_404(
        Activity,
        id=id,
        faculty=request.user
    )

    file = request.FILES.get("file")
    title = request.POST.get("title", "").strip()

    if file:
        ActivityMedia.objects.create(
            activity=activity,
            title=title or file.name,
            file=file
        )

    return redirect("activity_workspace", id=activity.id)


@require_POST
@login_required
def delete_media(request, media_id):
    media = get_object_or_404(
        ActivityMedia,
        id=media_id,
        activity__faculty=request.user
    )

    activity_id = media.activity.id
    media.delete()
    return redirect("activity_workspace", id=activity_id)


@login_required
def notification_hub(request, id):
    activity = get_object_or_404(Activity, id=id, faculty=request.user)

    draft_count = ActivityNotification.objects.filter(
        activity=activity, sender=request.user, status="draft"
    ).count()

    sent_count = ActivityNotification.objects.filter(
        activity=activity, sender=request.user, status="sent"
    ).count()

    return render(
        request,
        "activities_app/faculty/notification_hub.html",
        {
            "activity": activity,
            "draft_count": draft_count,
            "sent_count": sent_count,
        }
    )


@login_required
def compose_notification(request, id):
    activity = get_object_or_404(Activity, id=id, faculty=request.user)

    if request.method == "POST":
        status = "sent" if "send" in request.POST else "draft"

        ActivityNotification.objects.create(
            activity=activity,
            sender=request.user,
            subject=request.POST["subject"],
            message=request.POST["message"],
            notification_type=request.POST["notification_type"],
            send_email=bool(request.POST.get("send_email")),
            send_in_app=True,
            status=status,
        )

        return redirect(
            "notification_sent" if status == "sent" else "notification_drafts",
            id=id
        )

    return render(
        request,
        "activities_app/faculty/compose_notification.html",
        {"activity": activity}
    )


@login_required
def notification_drafts(request, id):
    activity = get_object_or_404(Activity, id=id, faculty=request.user)

    drafts = ActivityNotification.objects.filter(
        activity=activity,
        sender=request.user,
        status="draft"
    )

    return render(
        request,
        "activities_app/faculty/notification_drafts.html",
        {
            "activity": activity,
            "drafts": drafts
        }
    )


@login_required
def notification_sent(request, id):
    activity = get_object_or_404(Activity, id=id, faculty=request.user)

    sent = ActivityNotification.objects.filter(
        activity=activity,
        sender=request.user,
        status="sent"
    )

    return render(
        request,
        "activities_app/faculty/notification_sent.html",
        {
            "activity": activity,
            "sent": sent
        }
    )

@login_required
def faculty_feedback(request, id):
    activity = get_object_or_404(Activity, id=id, faculty=request.user)

    feedbacks = activity.feedbacks.order_by("-created_at")

    return render(
        request,
        "activities_app/faculty/faculty_feedback.html",
        {
            "activity": activity,
            "feedbacks": feedbacks
        }
    )



# ======================
# HELPERS
# ======================

def generate_fake_attendance(activity, student):
    fake_records = []
    for i in range(30):
        date = datetime.now().date() - timedelta(days=29 - i)
        if date.weekday() == 6:
            continue
        probability = 0.6 + (i / 30) * 0.3
        status = "Present" if random.random() < probability else "Absent"
        fake_records.append({"date": date, "status": status})
    return fake_records


# ======================
# STUDENT VIEWS (RESTORED)
# ======================

def browse_activities(request):
    activities = Activity.objects.all()

    registered_activity_ids = []
    if request.user.is_authenticated:
        registered_activity_ids = ActivityRegistration.objects.filter(
            student=request.user
        ).values_list("activity_id", flat=True)

    return render(
        request,
        "activities_app/student/browse_activities.html",
        {
            "activities": activities,
            "registered_activity_ids": registered_activity_ids
        }
    )

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def download_students(request, activity_id):
    return HttpResponse("Student download coming soon")


# ======================
# FACULTY RESOURCE REQUESTS
# ======================

@login_required
def faculty_resource_hub(request, id):
    activity = get_object_or_404(Activity, id=id, faculty=request.user)

    pending_count = ResourceRequest.objects.filter(
        activity=activity,
        sender=request.user,
        status="pending"
    ).count()

    approved_count = ResourceRequest.objects.filter(
        activity=activity,
        sender=request.user,
        status="approved"
    ).count()

    rejected_count = ResourceRequest.objects.filter(
        activity=activity,
        sender=request.user,
        status="rejected"
    ).count()

    requests = ResourceRequest.objects.filter(
        activity=activity,
        sender=request.user
    ).order_by("-created_at")

    return render(
        request,
        "activities_app/faculty/resource_hub.html",
        {
            "activity": activity,
            "requests": requests,
            "pending": pending_count,
            "approved": approved_count,
            "rejected": rejected_count,
        }
    )


@login_required
def create_resource_request(request, id):
    activity = get_object_or_404(Activity, id=id, faculty=request.user)

    if request.method == "POST":
        ResourceRequest.objects.create(
            activity=activity,
            sender=request.user,
            resource_type=request.POST["resource_type"],
            quantity=request.POST.get("quantity"),
            description=request.POST["description"],
        )

        messages.success(request, "Resource request sent successfully.")
        return redirect("faculty_resource_hub", id=activity.id)

    return render(
        request,
        "activities_app/faculty/resource_create.html",
        {"activity": activity}
    )


@login_required
def sent_resource_requests(request):
    requests = ResourceRequest.objects.filter(
        sender=request.user
    ).order_by("-created_at")

    return render(
        request,
        "activities_app/faculty/resource_sent.html",
        {"requests": requests}
    )

import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Activity, ActivityRegistration


@login_required
def download_students(request, activity_id):
    # ✅ Ensure faculty owns this activity
    activity = get_object_or_404(
        Activity,
        id=activity_id,
        faculty=request.user
    )

    registrations = ActivityRegistration.objects.filter(
        activity=activity
    ).select_related("student")

    # ✅ Create CSV response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{activity.title}_students.csv"'
    )

    writer = csv.writer(response)

    # Header row
    writer.writerow(["Name", "Username", "Email"])

    # Data rows
    for reg in registrations:
        student = reg.student
        writer.writerow([
            student.get_full_name() or "",
            student.username,
            student.email,
        ])

    return response
