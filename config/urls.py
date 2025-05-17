from django.contrib import admin
from django.urls import path, include
from students.views import welcome
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', welcome, name='welcome'),  # Home / Landing page
    path('admin/', admin.site.urls),    # Admin panel
    path('students/', include('students.urls')),  # Student app
]

# For media file handling (profile photos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
