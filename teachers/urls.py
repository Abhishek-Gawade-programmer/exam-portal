from django.urls import path
from .views import (create_new_test,create_new_subject)


urlpatterns = [
        path('test-create/',create_new_test,name ='test_create'),
        path('subject-create/',create_new_subject,name ='subject_create'),
        ]