from django.urls import path
from .views import (initial_setup,save_question,navigation_question,get_all_question_details)


urlpatterns = [
        path('',initial_setup,name ='quiz-list'),
        path('save-question/',save_question,name ='save_question'),
        path('get-all-question-details/',get_all_question_details,name ='get_all_question_details'),

        
        path('navigation-question/',navigation_question,name ='navigation_question')
        ]