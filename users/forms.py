from django import forms
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'roll_number',
            'smart_card_id',
            'department',
            'year',
            'section',
            'phone_number',
            'hostel',
            'course',
            'photograph',
        ]
from .models import FacultyProfile
from django import forms


class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        fields = [
            "faculty_id",
            "department",
            "designation",
            "phone_number",
            "photograph",
        ]
