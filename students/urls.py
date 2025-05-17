from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.student_register, name='student_register'),
    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.student_logout, name='student_logout'),
]
