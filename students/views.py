from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import datetime
from .models import Student, Attendance, Grade, Notice

def welcome(request):
    return render(request, 'welcome.html')

def student_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        roll_number = request.POST.get('roll_number')
        class_name = request.POST.get('class_name')
        dob_str = request.POST.get('date_of_birth')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'students/register.html')

        if Student.objects.filter(roll_number=roll_number).exists():
            messages.error(request, "Roll number already registered.")
            return render(request, 'students/register.html')

        try:
            date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return render(request, 'students/register.html')

        with transaction.atomic():
            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name)
            Student.objects.create(user=user, roll_number=roll_number,
                                   class_name=class_name, date_of_birth=date_of_birth)

        messages.success(request, "Registration successful! Please login.")
        return redirect('student_login')

    return render(request, 'students/register.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('student_dashboard')
        else:
            return render(request, 'students/login.html', {'error': 'Invalid username or password'})
    return render(request, 'students/login.html')

@login_required(login_url='student_login')
def student_dashboard(request):
    student = Student.objects.get(user=request.user)

    # Get selected semester from GET request (default to 1 if not provided)
    selected_semester = int(request.GET.get('semester', 1))

    # Filter attendance and grades by selected semester
    attendance_records = Attendance.objects.filter(student=student, semester=selected_semester)
    grades = Grade.objects.filter(student=student, semester=selected_semester)

    # Summary calculations
    present_count = attendance_records.filter(status='Present').count()
    absent_count = attendance_records.filter(status='Absent').count()
    total_subjects = grades.count()
    total_marks = sum(grade.marks for grade in grades)
    average_marks = round(total_marks / total_subjects, 2) if total_subjects else 0

    # Notices
    notices = Notice.objects.order_by('-created_at')[:5]

    context = {
        'student': student,
        'attendance_records': attendance_records,
        'grades': grades,
        'notices': notices,
        'present_count': present_count,
        'absent_count': absent_count,
        'average_marks': average_marks,
        'selected_semester': selected_semester,
        'semesters': range(1, 9),  # 1 to 8
    }
    return render(request, 'students/dashboard.html', context)

@login_required(login_url='student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        if photo:
            student.photo = photo
            student.save()
            messages.success(request, "Profile photo updated!")
        return redirect('student_dashboard')
    return render(request, 'students/edit_profile.html', {'student': student})

def student_logout(request):
    logout(request)
    return redirect('student_login')
