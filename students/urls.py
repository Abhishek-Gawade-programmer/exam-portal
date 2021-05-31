from django.urls import path
from .views import (initial_setup,save_question,navigation_question)


urlpatterns = [
        path('',initial_setup,name ='quiz-list'),
        path('save-question/',save_question,name ='save_question'),
        path('navigation-question/',navigation_question,name ='navigation_question')
        ]