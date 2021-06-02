from django.shortcuts import render,get_object_or_404
from django.views.generic.list import ListView
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.core.paginator import Paginator

from .models import *
from django.middleware.csrf import get_token
from django.utils import timezone
import json

def initial_setup(request):    
    all_user_question=Question.objects.order_by('?')
    all_user_question_ids=[]
    for each_question in all_user_question:
        if not StudentAnswer.objects.filter(question=each_question,test=each_question.test,student=request.user).exists():

            intial_student_answer=StudentAnswer.objects.create(question=each_question,test=each_question.test,student=request.user)
            intial_student_answer.save()

        if str(each_question.id) not in all_user_question_ids:
            all_user_question_ids.append(str(each_question.id))

    if not UserQuestionList.objects.filter(test=all_user_question[0].test,student=request.user).exists():

        student_test_data=UserQuestionList.objects.create(test=all_user_question[0].test,
                        student=request.user,test_question=json.dumps(all_user_question_ids),
                        start_time=timezone.now())
        student_test_data.save()

    return render(request,'home.html')

def save_question(request):
    if request.method=='POST' :
        question=get_object_or_404(Question,id=request.POST.get('pk'))
        student_answer=StudentAnswer.objects.get(question=question,test=question.test,student=request.user)
        print(student_answer)
        student_answer.student_option=request.POST.get('option')
        student_answer.save()
        return JsonResponse({'success':'true'},safe=False)
    return JsonResponse({'success':'false'})







def get_all_question_details(request):

    if request.method=='GET' :
        all_question_student=json.loads(UserQuestionList.objects.get(
                        student=request.user).test_question)

        all_question_json={}
        for i in range(len(all_question_student)):
            x=StudentAnswer.objects.get(student=request.user,question=all_question_student[i])
            all_question_json[i]={'seen':x.question_seen,'bookmark':x.bookmark,'student_option':x.student_option}


        return JsonResponse({'success':'true','all_question_json':all_question_json},safe=False)
    return JsonResponse({'success':'true','yes':'usidhb'},safe=False)




def navigation_question(request):
    page_number=int(request.POST.get('page_number'))-1




    if page_number == len(Question.objects.all()):
        return JsonResponse({
            'success':'true',
            'next':'false'
            },safe=False)
    question_id=json.loads(UserQuestionList.objects.get(student=request.user).test_question)[page_number]
    question=get_object_or_404(Question,id=question_id)

    student_answer=StudentAnswer.objects.get(question=question,test=question.test,student=request.user)
    print(student_answer)
    student_answer.question_seen=True
    student_answer.save()


    data_for_new_question={
        'success':'true',
        'question_title':question.question_title,
        'id':question.id,
        'option_1':{'text':question.option_1,'student_option':''},
        'option_2':{'text':question.option_2,'student_option':''},
        'option_3':{'text':question.option_3,'student_option':''},
        'option_4':{'text':question.option_4,'student_option':''},
        'csrf_token':get_token(request),

        }
    if StudentAnswer.objects.filter(question=question,test=question.test,student=request.user).exists():
        student_option= StudentAnswer.objects.get(question=question,test=question.test).student_option
        if student_option:
            data_for_new_question[f'option_{student_option}']['student_option']='checked'

    return JsonResponse(data_for_new_question,safe=False)






