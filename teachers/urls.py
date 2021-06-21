from django.urls import path
from .views import (create_new_test,create_new_subject,
                subject_list_view,subject_detail_view,
                create_new_question,test_detail_view,subject_update_view,
                test_update_view,question_update_view,for_hod_subject_list_view,show_all_student,
                verify_the_student,student_update_view,delete_the_question)

from students.views import TeacherSignUpView
urlpatterns = [
        path('teacher-signup/',TeacherSignUpView.as_view(), name='teacher_signup'),
        path('<int:pk>/test-create/',create_new_test,name ='test_create'),

        path('<int:test_id>/question-create/',create_new_question,name ='question_create'),
        path('<int:test_id>/<str:add_another>/question-create/',create_new_question,name ='question_create_add_another'),

        path('subject-create/',create_new_subject,name ='subject_create'),
        path('my-subject/',subject_list_view,name ='my_subject'),

        path('verify-student/<int:pk>/',verify_the_student,name ='verify_student'),
        
        path('delete-question/<uuid:pk>/',delete_the_question,name ='delete_the_question'),

        path('all-subject/',for_hod_subject_list_view,name ='all_subject'),
        path('subject-detail/<int:pk>/',subject_detail_view,name ='subject_detail'),
        path('subject-update/<int:pk>/',student_update_view,name ='subject_update'),

         path('my-students/',show_all_student,name ='my_students'),
         
        path('test-detail/<int:pk>/',test_detail_view,name ='test_detail'),


        path('subject-update/<int:pk>/',subject_update_view,name ='subject_update'),
        path('test-update/<int:pk>/',test_update_view,name ='test_update'),
        path('question-update/<uuid:pk>/',question_update_view,name ='question_update'),
        ]