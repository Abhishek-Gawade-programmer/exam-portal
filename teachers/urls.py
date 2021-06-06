from django.urls import path
from .views import (create_new_test,create_new_subject,
                subject_list_view,subject_detail_view,
                create_new_question,test_detail_view)


urlpatterns = [
        path('<int:pk>/test-create/',create_new_test,name ='test_create'),

        path('<int:test_id>/question-create/',create_new_question,name ='question_create'),

        path('subject-create/',create_new_subject,name ='subject_create'),
        path('all-subject/',subject_list_view,name ='all_subject'),
        path('subject-detail/<int:pk>/',subject_detail_view,name ='subject_detail'),

        path('test-detail/<int:pk>/',test_detail_view,name ='test_detail'),
        ]