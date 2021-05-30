from django.shortcuts import render,get_object_or_404
from django.views.generic.list import ListView
from django.http import JsonResponse, HttpResponse

from django.core.paginator import Paginator

from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

class QuestionList(ListView):
  
    # specify the model for list view
    model = Question
    context_object_name = 'all_question'
    template_name='home.html'
    paginate_by = 1


def save_question(request):
    if request.method=='POST' :
        question=get_object_or_404(Question,id=request.POST.get('pk'))
        student_answer=StudentAnswer.objects.get_or_create(question=question,test=question.test)
        student_answer[0].correct_option=request.POST.get('option')
        student_answer[0].save()
        return JsonResponse({'success':'true'},safe=False)
    return JsonResponse({'success':'false'})




def navigation_question(request):
    page_number=int(request.POST.get('page_number'))-1


    if page_number == len(Question.objects.all()):
        return JsonResponse({
            'success':'true',
            'next':'false'
            },safe=False)
    question=Question.objects.all()[page_number]



    return JsonResponse({
        'success':'true',
        'question_title':question.question_title,
        'id':question.id,
        'option_1':question.option_1,
        'option_2':question.option_2,
        'option_3':question.option_3,
        'option_4':question.option_4,
        'csrf_token':get_token(request),

        },safe=False)








    # print('jksdbhjsbdhjgfbsdufbisdbfsbd',page_number)


    # all_question=Question.objects.all()
    # paggge=Paginator(all_question,1)
    # paggge_obj=paggge.page(page_number)
    # print(paggge_obj.has_previous())
    # print(paggge_obj.has_next())
    # print(paggge_obj.next_page_number())

    # question_object=paggge_obj.object_list
    # print(question_object,'jksdfjksdbfdbsu554eqw5e4q524135')
    # return JsonResponse({'question//':'true'},safe=False)


    # if request.method=='POST' :
    #     question=get_object_or_404(Question,id=request.POST.get('pk'))
    #     student_answer=StudentAnswer.objects.get_or_create(question=question,test=question.test)
    #     student_answer[0].correct_option=request.POST.get('option')
    #     student_answer[0].save()
    # return JsonResponse({'success':'true'},safe=False)
    # return JsonResponse({'success':'false'})