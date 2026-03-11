from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import StudentProfileForm
from .models import StudentProfile


@login_required
def complete_student_profile(request):
    try:
        profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            student_profile = form.save(commit=False)
            student_profile.user = request.user

            # ✅ CORRECT FIELD (EXISTING IN DB)
            student_profile.is_profile_complete = True

            student_profile.save()

            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            return redirect('/student/dashboard/')
        else:
            print("FORM ERRORS:", form.errors)

    else:
        form = StudentProfileForm(instance=profile)

    return render(
        request,
        'users/student_profile.html',
        {
            'form': form,
            'user': request.user,
            'profile': profile
        }
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import FacultyProfile
from .forms import FacultyProfileForm


@login_required
def complete_faculty_profile(request):
    try:
        profile = request.user.faculty_profile
    except FacultyProfile.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = FacultyProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            faculty_profile = form.save(commit=False)
            faculty_profile.user = request.user

            # ✅ CORRECT FIELD (EXISTING IN DB)
            faculty_profile.is_profile_complete = True

            faculty_profile.save()

            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("/faculty/dashboard/")
    else:
        form = FacultyProfileForm(instance=profile)

    return render(
        request,
        "users/faculty_profile.html",
        {
            "form": form,
            "user": request.user,
            "profile": profile,
        }
    )
