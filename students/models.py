from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=20)
    year = models.IntegerField(choices=[(i, f"{i}st Year") for i in range(1, 5)])  # 1 to 4
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    semester = models.IntegerField(choices=[(i, f"Sem {i}") for i in range(1, 9)], default=1)

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    marks = models.FloatField()
    semester = models.IntegerField(choices=[(i, f"Sem {i}") for i in range(1, 9)], default=1)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject} (Sem {self.semester}): {self.marks}"

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
