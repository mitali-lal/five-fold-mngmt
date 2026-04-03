from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    fold = models.CharField(max_length=50)

    total_seats = models.IntegerField()
    filled_seats = models.IntegerField()

    schedule = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    quick_notes = models.TextField(blank=True)

    fee = models.PositiveIntegerField(default=0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    faculty = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="activities"
    )

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
    EXPERIENCE_CHOICES = [
        ("well_organized", "Well Organized"),
        ("fun", "Fun & Enjoyable"),
        ("informative", "Informative"),
        ("too_long", "Too Long"),
        ("poor_management", "Poor Management"),
    ]

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="feedbacks"
    )

    rating = models.PositiveIntegerField()
    experience = models.CharField(
    max_length=50,
    choices=EXPERIENCE_CHOICES
)

    created_at = models.DateTimeField(auto_now_add=True)
   


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


class ActivityNotification(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
    ]

    NOTIFICATION_TYPES = [
        ("update", "Activity Update"),
        ("reminder", "Reminder"),
        ("important", "Important Announcement"),
    ]

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    subject = models.CharField(max_length=255)
    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft"
    )

    send_email = models.BooleanField(default=False)
    send_in_app = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} ({self.status})"

class StudentNotificationReadStatus(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(ActivityNotification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'notification']


class ResourceRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    RESOURCE_TYPES = [
        ("equipment", "Equipment"),
        ("infrastructure", "Infrastructure"),
        ("transport", "Transport"),
        ("budget", "Budget"),
        ("other", "Other"),
    ]

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    resource_type = models.CharField(
        max_length=30,
        choices=RESOURCE_TYPES
    )

    description = models.TextField()
    quantity = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    admin_remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity.title} - {self.resource_type} ({self.status})"

class FacultyTimeSlot(models.Model):
    DAYS = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
        ("Sun", "Sunday"),
    ]

    faculty = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="time_slots"
    )

    activity = models.ForeignKey(
    "Activity",
    on_delete=models.CASCADE,
    related_name="time_slots",
    null=True,
    blank=True
)


    day = models.CharField(max_length=3, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    

    def __str__(self):
        return f"{self.activity.title} | {self.day} {self.start_time}-{self.end_time}"


    class Meta:
        ordering = ["day", "start_time"]

    def __str__(self):
        return f"{self.faculty.username} | {self.day} {self.start_time}-{self.end_time}"
