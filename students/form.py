from django import forms
from .models import Student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'class_name', 'year', 'date_of_birth', 'photo']
