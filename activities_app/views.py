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
        experience=request.POST.get("experience")
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


from django.db.models import Avg   # ✅ ADD THIS AT TOP (once)

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

    # ✅ ADD THIS (AVERAGE CALCULATION)
    avg_rating = activity.feedbacks.aggregate(avg=Avg("rating"))["avg"]

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
            "back_url": back_url,
            "avg_rating": avg_rating,   # ✅ ADD THIS LINE
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

    from django.contrib.auth.models import User

    student_username = request.GET.get("student")

    if student_username:
        student_obj = User.objects.get(username=student_username)
    else:
        student_obj = request.user

    # Fetch records
    records = Attendance.objects.filter(
        activity=activity,
        student=student_obj
    ).order_by("date")

    # ✅ CORRECT INDENTATION (INSIDE FUNCTION)
    if not records.exists():
        generate_fake_attendance(activity, student_obj)

        records = Attendance.objects.filter(
            activity=activity,
            student=student_obj
        ).order_by("date")

    # Stats
    present = records.filter(status="Present").count()
    absent = records.filter(status="Absent").count()
    total = present + absent

    percent = int((present / total) * 100) if total > 0 else 0

    context = {
        "activity": activity,
        "attendance_records": records,
        "present": present,
        "absent": absent,
        "total_sessions": total,
        "percent": percent,
    }

   
    return render(request, "activities_app/student/attendance_panel.html", context)


from django.contrib.auth.models import User

@login_required
def student_attendance_api(request, id):
    activity = get_object_or_404(Activity, id=id)

    from django.contrib.auth.models import User
    student_username = request.GET.get("student")
    student_obj = User.objects.get(username=student_username)

    records = Attendance.objects.filter(
        activity=activity,
        student=student_obj
    ).order_by("date")

    # ALWAYS ensure full data exists
    generate_fake_attendance(activity, student_obj)

    records = Attendance.objects.filter(
        activity=activity,
        student=student_obj
    ).order_by("date")

    present = records.filter(status="Present").count()
    absent = records.filter(status="Absent").count()
    total = present + absent
    percent = int((present / total) * 100) if total > 0 else 0

    context = {
        "activity": activity,
        "attendance_records": records,
        "present": present,
        "absent": absent,
        "total_sessions": total,
        "percent": percent,
    }

    # ✅ THIS MUST BE INDENTED
    return render(request, "activities_app/student/_attendance_content.html", context)
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

    from django.contrib.auth.models import User

    registrations = ActivityRegistration.objects.filter(
        activity=activity
).exclude(student__is_superuser=True)

    students = []

    for reg in registrations:
        user = reg.student

        records = Attendance.objects.filter(
            activity=activity,
            student=user
        )

        present = records.filter(status="Present").count()
        absent = records.filter(status="Absent").count()
        total = present + absent

        percent = int((present / total) * 100) if total > 0 else 0

        students.append({
            "name": user.get_full_name() or user.username,
            "roll_no": user.username,  # temporary
            "email": user.email,
            "attendance": percent,
        })

    total_students = len(students)
    present_today = sum(1 for s in students if s["attendance"] >= 50)
    absent_today = total_students - present_today

    return render(
        request,
        "activities_app/faculty/faculty_attendance.html",
        {
            "activity": activity,
            "students": students,
            "present_today": present_today,
            "absent_today": absent_today,
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
    from datetime import date, timedelta
    import random

    # ✅ get registration
    registration = ActivityRegistration.objects.get(
        activity=activity,
        student=student
    )

    # ✅ CORRECT FIELD NAME
    start_date = registration.registered_at.date()
    today = date.today()

    random.seed(str(student.username))

    current = start_date

    while current <= today:

        # skip Tuesday (same as your logic)
        if current.weekday() != 1:

            status = "Present" if random.random() > 0.25 else "Absent"

            Attendance.objects.get_or_create(
                activity=activity,
                student=student,
                date=current,
                defaults={"status": status}
            )

        current += timedelta(days=1)


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
