from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect  # ✅ ADD THIS IMPORT

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("auth_app.urls")),
    path("activities/", include("activities_app.urls")),
    
    # ✅ FIXED: Redirect /activity/ to /activities/student/activity/
    path('activity/<int:id>/', lambda request, id: redirect(f'/activities/student/activity/{id}/')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )