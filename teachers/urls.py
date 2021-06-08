from django.urls import path
from .views import (create_new_test,create_new_subject,
                subject_list_view,subject_detail_view,
                create_new_question,test_detail_view,subject_update_view,
                test_update_view,question_update_view)

from students.views import TeacherSignUpView
urlpatterns = [
        path('teacher-signup/',TeacherSignUpView.as_view(), name='teacher_signup'),
        path('<int:pk>/test-create/',create_new_test,name ='test_create'),

        path('<int:test_id>/question-create/',create_new_question,name ='question_create'),

        path('subject-create/',create_new_subject,name ='subject_create'),
        path('all-subject/',subject_list_view,name ='all_subject'),
        path('subject-detail/<int:pk>/',subject_detail_view,name ='subject_detail'),

        path('test-detail/<int:pk>/',test_detail_view,name ='test_detail'),


        path('subject-update/<int:pk>/',subject_update_view,name ='subject_update'),
        path('test-update/<int:pk>/',test_update_view,name ='test_update'),
        path('question-update/<uuid:pk>/',question_update_view,name ='question_update'),
        ]