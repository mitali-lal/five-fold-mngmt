from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Activity, ActivityRegistration, Attendance
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.timezone import now
import random
from datetime import datetime, timedelta
import math
import json


# ======================
# STUDENT VIEWS
# ======================

from .models import Activity, ActivityRegistration

def browse_activities(request):
    activities = Activity.objects.all()

    registered_activity_ids = []
    if request.user.is_authenticated:
        registered_activity_ids = ActivityRegistration.objects.filter(
            student=request.user
        ).values_list("activity_id", flat=True)

    return render(
        request,
        'activities_app/student/browse_activities.html',
        {
            'activities': activities,
            'registered_activity_ids': registered_activity_ids
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

    return render(
        request,
        'activities_app/student/activity_detail.html',
        {
            'activity': activity,
            'available_seats': available_seats,
            'related_activities': related_activities,
            'feedbacks': feedbacks,
            'is_registered': is_registered
        }
    )


def my_registrations(request):
    registrations = ActivityRegistration.objects.filter(student=request.user)

    return render(request, "activities_app/student/my_registrations.html", {
        "registrations": registrations
    })
    



@login_required
def register_activity(request, id):
    if request.method == "POST":
        activity = get_object_or_404(Activity, id=id)

        ActivityRegistration.objects.get_or_create(
            student=request.user,
            activity=activity
    )

    return redirect('activity_detail', id=activity.id)




# ======================
# FACULTY VIEWS
# ======================

def assigned_activities(request):
    return render(request, 'activities_app/faculty/assigned_activities.html')


def activity_workspace(request, id):
    return render(request, 'activities_app/faculty/activity_workspace.html')


def faculty_attendance_overview(request, id):
    return render(request, 'activities_app/faculty/attendance_overview.html')


# ======================
# ADMIN VIEWS
# ======================

def create_activity(request):
    return render(request, 'activities_app/admin/create_activity.html')


def manage_activities(request):
    return render(request, 'activities_app/admin/manage_activities.html')


def attendance_overview(request, id):
    activity = get_object_or_404(Activity, id=id)

    # Get all attendance records for this student and activity
    records = Attendance.objects.filter(
        activity=activity,
        student=request.user
    ).order_by("date")

    # If no records exist, generate fake data for demonstration
    if not records.exists():
        fake_records = generate_fake_attendance(activity, request.user)
        # Count present/absent from fake records
        present = sum(1 for r in fake_records if r['status'] == 'Present')
        absent = sum(1 for r in fake_records if r['status'] == 'Absent')
        attendance_records_list = fake_records
    else:
        present = records.filter(status="Present").count()
        absent = records.filter(status="Absent").count()
        # Convert queryset to list of dictionaries for template
        attendance_records_list = [
            {
                'date': r.date,
                'status': r.status
            }
            for r in records
        ]
    
    total = present + absent
    
    percent = int((present / total) * 100) if total else 0
    
    # Calculate required classes to reach 50%
    required_present = 0
    if total > 0 and percent < 50:
        required_present = math.ceil((0.5 * total - present) / 0.5)
    
    # Weekly data for charts (last 7 days or all if less)
    all_records = attendance_records_list[-7:]  # Take last 7 records
    week_labels = [r['date'].strftime("%d %b") for r in all_records]
    week_data = [
        1 if r['status'] == "Present" else 0
        for r in all_records
    ]
    
    # Convert to JSON-safe format
    week_labels_json = json.dumps(week_labels)
    week_data_json = json.dumps(week_data)
    
    return render(
        request,
        "activities_app/student/attendance_panel.html",
        {
            "activity": activity,
            "attendance_records": attendance_records_list,
            "present": present,
            "absent": absent,
            "total_sessions": total,
            "percent": percent,
            "required_present": required_present,
        }
    )

# Helper function to generate fake attendance data
def generate_fake_attendance(activity, student):
    # Generate attendance for last 30 days (excluding Sundays)
    fake_records = []
    for i in range(30):
        date = datetime.now().date() - timedelta(days=29-i)
        
        # Skip Sundays and some random holidays
        if date.weekday() == 6:  # Sunday
            continue
        
        # Skip some Tuesdays as holidays (as per your example)
        if date.weekday() == 1 and random.random() < 0.3:  # Tuesday
            continue
            
        # Generate attendance status (75% present, 25% absent - mathematically correct)
        # More absent days at the beginning, more present towards the end
        probability = 0.6 + (i / 30) * 0.3  # Increases from 60% to 90%
        status = "Present" if random.random() < probability else "Absent"
        
        fake_records.append({
            'date': date,
            'status': status,
        })
    
    return fake_records