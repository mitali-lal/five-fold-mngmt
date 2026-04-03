from django.contrib import admin
from .models import (
    Activity,
    ActivityMedia,
    Feedback,
    ActivityRegistration,
    Attendance,
    ActivityNotification,
    ResourceRequest,
    StudentNotificationReadStatus,
    FacultyTimeSlot,
    Requirement
)


class ActivityMediaInline(admin.TabularInline):
    model = ActivityMedia
    extra = 0


class ActivityRegistrationInline(admin.TabularInline):
    model = ActivityRegistration
    extra = 0
    readonly_fields = ("student", "registered_at")


class RequirementInline(admin.TabularInline):
    model = Requirement
    extra = 1


class TimeSlotInline(admin.TabularInline):
    model = FacultyTimeSlot
    extra = 1


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "fold",
        "fee",
        "total_seats",
        "filled_seats",
    )
    search_fields = ("title",)
    list_filter = ("fold",)
    ordering = ("fold", "title")
    inlines = [
    ActivityMediaInline,
    ActivityRegistrationInline,
    RequirementInline,   # ✅ ADD THIS
    TimeSlotInline,      # ✅ ADD THIS
]


@admin.register(ActivityMedia)
class ActivityMediaAdmin(admin.ModelAdmin):
    list_display = ("title", "activity")
    search_fields = ("title",)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("activity", "rating", "created_at")
    list_filter = ("rating",)
    date_hierarchy = "created_at"


@admin.register(ActivityRegistration)
class ActivityRegistrationAdmin(admin.ModelAdmin):
    list_display = ("student", "activity", "registered_at")
    list_filter = ("activity",)
    search_fields = ("student__username", "activity__title")
    date_hierarchy = "registered_at"

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "activity", "date", "status")
    list_filter = ("status", "activity")
    search_fields = ("student__username",)


@admin.register(ActivityNotification)
class ActivityNotificationAdmin(admin.ModelAdmin):
    list_display = ("activity", "subject", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("subject",)
    date_hierarchy = "created_at"


@admin.register(ResourceRequest)
class ResourceRequestAdmin(admin.ModelAdmin):
    list_display = ("activity", "sender", "resource_type", "status")
    list_filter = ("status", "resource_type")
    search_fields = ("sender__username",)


@admin.register(StudentNotificationReadStatus)
class StudentNotificationReadStatusAdmin(admin.ModelAdmin):
    list_display = ("student", "notification", "is_read")
    list_filter = ("is_read",)


@admin.register(FacultyTimeSlot)
class FacultyTimeSlotAdmin(admin.ModelAdmin):
    list_display = ("faculty", "day", "start_time", "end_time")
    list_filter = ("day",)


