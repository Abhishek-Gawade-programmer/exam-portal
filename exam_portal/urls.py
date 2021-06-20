from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from students.views import redirect_after_login
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', TemplateView.as_view(template_name="chose_your_signup.html"), name='signup'),
    path('admin/', admin.site.urls),
    path('teachers/', include('teachers.urls')),
    path('verification/', include('verify_email.urls')),

    path('redirect-user/', redirect_after_login,
        name='redirect_after_login'),

    path('', include('students.urls')),
]
