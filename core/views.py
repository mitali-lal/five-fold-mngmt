from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def home(request):
    role = None

    if request.user.is_authenticated:
        if request.user.is_superuser:
            role = 'admin'
        elif request.user.is_staff:
            role = 'faculty'
        else:
            role = 'student'

    return render(request, 'core/home.html', {'role': role})


@login_required
def dashboard_redirect(request):
    user = request.user

    if user.is_superuser:
        return redirect('/admin/dashboard/')
    elif user.is_staff:
        return redirect('/faculty/dashboard/')
    else:
        return redirect('/student/dashboard/')


def logout_user(request):
    logout(request)
    return redirect('home')
