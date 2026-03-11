from django.urls import path
from . import views

urlpatterns = [
    path(
        "profile/student/",
        views.complete_student_profile,
        name="student_profile",
    ),
    path(
        "profile/faculty/",
        views.complete_faculty_profile,
        name="faculty_profile",
    ),
]
