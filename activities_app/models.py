from django.db import models
from django.conf import settings


class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    fold = models.CharField(max_length=50)

    total_seats = models.IntegerField()
    filled_seats = models.IntegerField()

    schedule = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    quick_notes = models.TextField(blank=True)

    faculty_name = models.CharField(max_length=100, blank=True)
    faculty_email = models.EmailField(blank=True)

    fee = models.PositiveIntegerField(default=0)
    


    def __str__(self):
        return self.title


class ActivityMedia(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="media"
    )
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="activity_media/")

    def __str__(self):
        return f"{self.activity.title} - {self.title}"

class Feedback(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    rating = models.PositiveIntegerField()  # 1–5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity.title} - {self.rating}"

from django.conf import settings

class ActivityRegistration(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "activity")

    def __str__(self):
        return f"{self.student} → {self.activity.title}"
class Attendance(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[("Present", "Present"), ("Absent", "Absent")]
    )

    def __str__(self):
        return f"{self.student} - {self.activity} - {self.status}"

 

