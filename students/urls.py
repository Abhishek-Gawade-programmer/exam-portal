from django.urls import path
from .views import (initial_setup,save_question,navigation_question,get_all_question_details,toogle_bookmark)


urlpatterns = [
        path('',initial_setup,name ='quiz-list'),

        path('save-question/',save_question,name ='save_question'),
        path('get-all-question-details/',get_all_question_details,name ='get_all_question_details'),
        path('toogle-bookmark/<int:page_number>/',toogle_bookmark,name ='toogle_bookmark'),

        
        path('navigation-question/',navigation_question,name ='navigation_question')
        ]