from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),

    path('', include('core.urls')),

    # Auth
    path("", include("auth_app.urls")),

    # 🔹 ADMIN PANEL — MUST COME BEFORE activities/
    path("", include("activities_app.admin_urls")),

    path("admin-panel/", include("activities_app.admin_urls")),

    # 🔹 Student + Faculty
    path("activities/", include("activities_app.urls")),

    # Users
    path("users/", include("users.urls")),

    # Redirect old activity links
    path(
        "activity/<int:id>/",
        lambda request, id: redirect(f"/activities/student/activity/{id}/")
    ),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
