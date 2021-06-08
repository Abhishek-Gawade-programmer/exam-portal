from django.urls import path
from .views import (initial_setup,save_question,navigation_question,
                get_all_question_details,toogle_bookmark,report_question,
                submit_exam,StudentSignUpView)


urlpatterns = [
        path('student-signup/',StudentSignUpView.as_view(), name='student_signup'),
        path('',initial_setup,name ='quiz-list'),

        path('save-question/',save_question,name ='save_question'),
        
        path('submit-exam/',submit_exam,name ='submit_exam'),
        path('get-all-question-details/',get_all_question_details,name ='get_all_question_details'),
        path('toogle-bookmark/<int:page_number>/',toogle_bookmark,name ='toogle_bookmark'),
        path('report-question/<int:page_number>/<str:comment>/',report_question,name ='report_question'),

        
        path('navigation-question/',navigation_question,name ='navigation_question')
        ]