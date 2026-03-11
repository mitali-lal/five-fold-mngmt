from django.urls import path
from .views import home, dashboard_redirect, logout_user

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('logout/', logout_user, name='logout'),
]
