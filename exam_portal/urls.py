from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('teachers/', include('teachers.urls')),
    path('verification/', include('verify_email.urls')),    
    path('', include('students.urls')),
]
