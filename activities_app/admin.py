from django.contrib import admin
from .models import Activity, ActivityMedia
from .models import Feedback
from .models import ActivityRegistration

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'fold',
        'fee',
        'total_seats',
        'filled_seats',
    )
    search_fields = ('title', 'fold')
    list_filter = ('fold',)

@admin.register(ActivityMedia)
class ActivityMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('activity', 'rating', 'created_at')

@admin.register(ActivityRegistration)
class ActivityRegistrationAdmin(admin.ModelAdmin):
    list_display = ("student", "activity", "registered_at")
    list_filter = ("activity", "student")
    search_fields = ("student__username", "activity__title")