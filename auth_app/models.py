from django.db import models
from django.contrib.auth.models import User
import uuid

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - verified={self.email_verified}"

class Feedback(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="app_feedbacks")
    category = models.CharField(max_length=50)
    module = models.CharField(max_length=50)
    issue_type = models.CharField(max_length=50)

    description = models.TextField()
    expected = models.TextField(blank=True)

    priority = models.CharField(max_length=10)

    affected_users = models.CharField(max_length=50, blank=True)
    followup_preference = models.CharField(max_length=50, blank=True)
    additional_comments = models.TextField(blank=True)

    attachment = models.FileField(upload_to='feedback/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.user}"