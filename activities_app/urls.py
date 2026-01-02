from django.urls import path
from . import views

urlpatterns = [
    

    # STUDENT
    path('student/activities/', views.browse_activities, name='browse_activities'),
    path('student/registrations/', views.my_registrations, name='my_registrations'),
    path('student/activity/<int:id>/', views.activity_detail, name='activity_detail'),
    path('student/activity/<int:id>/register/', views.register_activity, name='register_activity'),
    # ATTENDANCE (USED BY STUDENT PANEL)
    path(
        'student/activity/<int:id>/attendance/',
        views.attendance_overview,
        name='attendance_overview'
    ),

    # FACULTY
    path('faculty/activities/', views.assigned_activities, name='assigned_activities'),
    path('faculty/activity/<int:id>/', views.activity_workspace, name='activity_workspace'),
     path(
        'faculty/activity/<int:id>/attendance/', 
        views.faculty_attendance_overview,  # CHANGED THIS
        name='faculty_attendance_overview'
    ),
    # ADMIN
    path('admin/activities/create/', views.create_activity, name='create_activity'),
    path('admin/activities/manage/', views.manage_activities, name='manage_activities'),
]
