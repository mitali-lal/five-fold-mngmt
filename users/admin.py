from django.contrib import admin
from .models import StudentProfile, FacultyProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "smart_card_id",
        "course",
        "hostel",
        "is_profile_complete",
    )
    list_filter = ("course", "hostel", "is_profile_complete")
    search_fields = ("user__username", "smart_card_id")
    ordering = ("user",)
    raw_id_fields = ("user",)


@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "is_profile_complete")
    list_filter = ("department", "is_profile_complete")
    search_fields = ("user__username",)
    raw_id_fields = ("user",)
