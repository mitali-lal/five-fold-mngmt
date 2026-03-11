from django.urls import path
from . import views
from . import admin_views


urlpatterns = [

    # ======================
    # STUDENT
    # ======================
    path('student/activities/', views.browse_activities, name='browse_activities'),
    path('student/registrations/', views.my_registrations, name='my_registrations'),
    path('student/activity/<int:id>/', views.activity_detail, name='activity_detail'),
    path('student/activity/<int:id>/register/', views.register_activity, name='register_activity'),
    path(
        'student/activity/<int:id>/attendance/',
        views.attendance_overview,
        name='attendance_overview'
    ),
    path(
    "student/notifications/",
    views.student_notifications,
    name="student_notifications"
),
path(
    "student/activity/<int:id>/feedback/",
    views.submit_feedback,
    name="submit_feedback"
),



    # ======================
    # FACULTY
    # ======================
    
    path(
        'faculty/activities/',
        views.assigned_activities,
        name='assigned_activities'
    ),

    path(
        'faculty/activity/<int:id>/',
        views.activity_workspace,
        name='activity_workspace'
    ),

    path(
        'faculty/activity/<int:id>/update/',
        views.update_activity,
        name='update_activity'
    ),

    path(
        'faculty/activity/<int:id>/media/add/',
        views.add_media,
        name='add_media'
    ),

    path(
        'faculty/activity/media/<int:media_id>/delete/',
        views.delete_media,
        name='delete_media'
    ),
    path(
    "faculty/activity/<int:id>/notifications/",
    views.notification_hub,
    name="notification_hub"
),
path(
    "faculty/activity/<int:id>/notifications/compose/",
    views.compose_notification,
    name="compose_notification"
),
path(
    "faculty/activity/<int:id>/notifications/drafts/",
    views.notification_drafts,
    name="notification_drafts"
),
path(
    "faculty/activity/<int:id>/notifications/sent/",
    views.notification_sent,
    name="notification_sent"
),
path(
    "faculty/activity/<int:id>/attendance/",
    views.faculty_attendance,
    name="faculty_attendance"
),
path(
    "faculty/activity/<int:id>/feedback/",
    views.faculty_feedback,
    name="faculty_feedback"
),
path(
    'faculty/activity/<int:activity_id>/download-students/',
    views.download_students,
    name='download_students'
),
# ======================
# FACULTY RESOURCE REQUEST URLS
# ======================

path(
    "faculty/resource/<int:id>/",
    views.faculty_resource_hub,
    name="faculty_resource_hub"
),

path(
    "faculty/resource/create/<int:id>/",
    views.create_resource_request,
    name="create_resource_request"
),

path(
    "faculty/resource/sent/",
    views.sent_resource_requests,
    name="sent_resource_requests"
),




]
