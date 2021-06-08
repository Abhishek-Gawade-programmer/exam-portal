from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse, HttpResponse

from students.models import *
from django.middleware.csrf import get_token
from django.utils import timezone
import json
from django.views.generic import ListView,DetailView,View,CreateView,UpdateView

from .forms import TestCreateFrom,SubjectCreateFrom,QuestionCreateFrom
from django.contrib import messages


def create_new_test(request,pk):
	subject=Subject.objects.get(pk=pk)
	testcreatefrom = TestCreateFrom()
	if request.method == 'POST':
		testcreatefrom = TestCreateFrom(request.POST)
		if testcreatefrom.is_valid():

			edit_testcreatefrom=testcreatefrom.save(commit=False)
			edit_testcreatefrom.subject=subject
			edit_testcreatefrom.teacher=request.user
			
			edit_testcreatefrom.save()

			messages.success(request, f"Test {edit_testcreatefrom.test_title} has been created add question in it")
			return redirect("subject_detail",pk=subject.id)

	return render(request,'teachers/create_new_test.html',{'testcreatefrom':testcreatefrom})



def create_new_subject(request):
	subjectcreatefrom = SubjectCreateFrom()
	if request.method == 'POST':
		subjectcreatefrom = SubjectCreateFrom(request.POST)
		if subjectcreatefrom.is_valid():
			edit_subjectcreatefrom=subjectcreatefrom.save(commit=False)
			edit_subjectcreatefrom.hod=request.user
			edit_subjectcreatefrom.save()
			messages.success(request, f"New Subject :: {edit_subjectcreatefrom.subject_name} has been created successfully")
			return redirect("all_subject")

	return render(request,'teachers/create_new_subject.html',{'subjectcreatefrom':SubjectCreateFrom})




def subject_list_view(request):
    all_subject=Subject.objects.all()
    return render(request,'teachers/all_subject_list.html',
    			{'all_subject':all_subject})


def subject_detail_view(request,pk):
    subject=Subject.objects.get(pk=pk)
    test_in_subject=Test.objects.filter(subject=subject)
    return render(request,'teachers/subject_detail.html',
    			{'subject':subject,'test_in_subject':test_in_subject})


def test_detail_view(request,pk):
    test=Test.objects.get(pk=pk)
    ques_in_test=Question.objects.filter(test=test)
    return render(request,'teachers/test_detail.html',
    			{'test':test,'ques_in_test':ques_in_test})



def create_new_question(request,test_id):
	test=Test.objects.get(id=test_id)
	questioncreatefrom = QuestionCreateFrom()
	if request.method == 'POST':
		questioncreatefrom = QuestionCreateFrom(request.POST)
		if questioncreatefrom.is_valid():
			edit_questioncreatefrom=questioncreatefrom.save(commit=False)
			edit_questioncreatefrom.teacher=request.user
			edit_questioncreatefrom.test=test
			edit_questioncreatefrom.save()
			messages.success(request, f"New Question creaeted :: {edit_questioncreatefrom.question_title} has been created successfully")
			return redirect("test_detail",pk=test.id)

	return render(request,'teachers/create_new_question.html',{'questioncreatefrom':questioncreatefrom,'test':test})



def subject_update_view(request, pk):
 
    subject_object = get_object_or_404(Subject, id = pk)
 
    subject_update_form = SubjectCreateFrom(request.POST or None, instance = subject_object)

    if subject_update_form.is_valid():
    	edit_subject_update_form=subject_update_form.save(commit=False)
    	edit_subject_update_form.hod=request.user
    	edit_subject_update_form.save()
    	messages.success(request, f"{edit_subject_update_form.subject_name} has been Updated successfully !!")
    	return redirect("all_subject")

 
    return render(request, "teachers/subject_update_form.html", {
    			'subject_update_form':subject_update_form,'subject':subject_object})




def test_update_view(request, pk):
 
    test_object = get_object_or_404(Test, id = pk)
 
    test_update_form = TestCreateFrom(request.POST or None, instance = test_object)

    if test_update_form.is_valid():
    	edit_test_update_form=test_update_form.save(commit=False)
    	edit_test_update_form.subject=test_object.subject
    	edit_test_update_form.teacher=request.user
    	edit_test_update_form.save()
    	messages.success(request, f"{test_object.test_title} has been Updated successfully !!")
    	return redirect("subject_detail",pk=test_object.subject.id)

 
    return render(request, "teachers/test_update_form.html", {
    			'test_update_form':test_update_form,'test':test_object})



def question_update_view(request, pk):
 
    question_object = get_object_or_404(Question, id = pk)
 
    question_update_form = QuestionCreateFrom(request.POST or None, instance = question_object)

    if question_update_form.is_valid():
    	edit_question_update_form=question_update_form.save(commit=False)
    	edit_question_update_form.teacher=request.user
    	edit_question_update_form.test=question_object.test
    	edit_question_update_form.save()
    	messages.success(request, f"{question_object.question_title} has been Updated successfully !!")
    	return redirect("test_detail",pk=question_object.test.id)

 
    return render(request, "teachers/question_update_form.html", {
    			'question_update_form':question_update_form,'question':question_object})
