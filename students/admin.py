from django.contrib import admin
from .models import Student, Attendance, Grade, Notice

admin.site.site_header = "Admin Login Portal"
admin.site.site_title = "Admin Login Portal"
admin.site.index_title = "Welcome to the Admin Portal"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'class_name', 'date_of_birth')
    search_fields = ('user__username', 'roll_number', 'class_name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('status', 'date')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks')
    search_fields = ('student__user__username', 'subject')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    ordering = ('-created_at',)
