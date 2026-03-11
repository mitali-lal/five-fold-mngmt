from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    roll_number = models.CharField(max_length=20, unique=True)
    smart_card_id = models.CharField(max_length=30, unique=True)

    department = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    section = models.CharField(max_length=10, blank=True, null=True)

    hostel = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    photograph = models.ImageField(upload_to='student_photos/')

    is_profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Student"


class FacultyProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='faculty_profile'
    )

    faculty_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)

    designation = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Faculty"

from django.conf import settings
from django.db import models


class FacultyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="faculty_profile"
    )

    faculty_id = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=100)

    designation = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    photograph = models.ImageField(
        upload_to="faculty_photos/",
        blank=True,
        null=True
    )

    is_profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.faculty_id})"
