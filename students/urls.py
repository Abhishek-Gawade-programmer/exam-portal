from django.urls import path
from .views import (QuestionList,save_question,navigation_question)


urlpatterns = [
        path('',QuestionList.as_view(),name ='quiz-list'),
        path('save-question/',save_question,name ='save_question'),
        path('navigation-question/',navigation_question,name ='navigation_question')
        ]