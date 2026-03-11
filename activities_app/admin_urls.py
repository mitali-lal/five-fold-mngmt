from django.urls import path
from . import admin_views

urlpatterns = [
    path(
        "admin-panel/activities/manage/",
        admin_views.manage_activities,
        name="admin_manage_activities",
    ),
    path(
        "admin-panel/activities/create/",
        admin_views.create_activity,
        name="admin_create_activity",
    ),
    path(
        "admin-panel/activity/<int:id>/edit/",
        admin_views.admin_edit_activity,
        name="admin_activity_edit",
    ),
    path(
        "admin-panel/activity/<int:id>/delete/",
        admin_views.admin_delete_activity,
        name="admin_delete_activity",
    ),
    path(
    "admin-panel/activities/bulk-action/",
    admin_views.admin_bulk_action,
    name="admin_bulk_action",
),
path(
    "admin-panel/activity/<int:id>/feedback/",
    admin_views.admin_activity_feedback,
    name="admin_activity_feedback",
),
 path(
        "resource-requests/",
        admin_views.admin_resource_requests,
        name="admin_resource_requests"
    ),
    path(
        "resource-requests/<int:id>/update/",
        admin_views.update_resource_request,
        name="update_resource_request"
    ),
    path(
    "admin-panel/students/",
    admin_views.admin_students_list,
    name="admin_students_list",
),
path(
    "admin-panel/students/<int:id>/",
    admin_views.admin_student_detail,
    name="admin_student_detail",
),

path(
    "admin-panel/students/<int:id>/edit/",
    admin_views.admin_student_edit,
    name="admin_student_edit",
),
path(
    "admin-panel/students/<int:id>/deactivate/",
    admin_views.admin_student_deactivate,
    name="admin_student_deactivate",
),
path(
    "admin-panel/students/add/",
    admin_views.admin_student_add,
    name="admin_student_add",
),
path(
    "admin-panel/students/export/pdf/",
    admin_views.admin_students_export_pdf,
    name="admin_students_export_pdf",
),
# ---------- FACULTY MANAGEMENT ----------

# ---------- FACULTY MANAGEMENT ----------

# HUB
path(
    "admin-panel/faculty/",
    admin_views.admin_faculty_hub,
    name="admin_faculty_hub",
),

# LIST (student-list style page)
path(
    "admin-panel/faculty/list/",
    admin_views.admin_faculty_list,
    name="admin_faculty_list",
),

# ASSIGN
path(
    "admin-panel/faculty/assign/",
    admin_views.admin_faculty_assign,
    name="admin_faculty_assign",
),

# DETAIL
path(
    "admin-panel/faculty/<int:id>/",
    admin_views.admin_faculty_detail,
    name="admin_faculty_detail",
),

# DEACTIVATE
path(
    "admin-panel/faculty/<int:id>/deactivate/",
    admin_views.admin_faculty_deactivate,
    name="admin_faculty_deactivate",
),
path(
    "admin-panel/notifications/",
    admin_views.admin_notifications,
    name="admin_notifications",
),
path(
    "admin-panel/audit-logs/",
    admin_views.audit_logs,
    name="audit_logs",
),
path(
    "admin-panel/system-settings/",
    admin_views.system_settings,
    name="system_settings",
),
path(
    "admin-panel/dashboard/",
    admin_views.admin_dashboard,
    name="admin_dashboard",
),

]
