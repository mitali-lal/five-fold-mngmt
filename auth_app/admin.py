from django.contrib import admin
from .models import EmailVerification
from .models import Feedback

admin.site.register(Feedback)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "email_verified", "created_at")
    list_filter = ("email_verified",)
