from django.urls import path
from .views import (create_new_test,create_new_subject,subject_list_view,subject_detail_view)


urlpatterns = [
        path('test-create/',create_new_test,name ='test_create'),
        path('subject-create/',create_new_subject,name ='subject_create'),
        path('all-subject/',subject_list_view,name ='all_subject'),
        path('subject-detail/<int:pk>/',subject_detail_view,name ='subject_detail'),
        ]