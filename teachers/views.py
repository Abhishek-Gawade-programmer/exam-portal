from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse, HttpResponse

from students.models import *
from django.middleware.csrf import get_token
from django.utils import timezone
import json
from django.views.generic import ListView,DetailView,View,CreateView,UpdateView

from .forms import TestCreateFrom,SubjectCreateFrom
from django.contrib import messages


def create_new_test(request):
	testcreatefrom = TestCreateFrom()
	if request.method == 'POST':
		testcreatefrom = TestCreateFrom(request.POST)
		if testcreatefrom.is_valid():
			testcreatefrom.save()
			messages.success(request, f"Test {testcreatefrom.test_title} has been created add question in it")
			#redirect to tect deatail and all quewstion view

	return render(request,'teachers/create_new_test.html',{'testcreatefrom':testcreatefrom})



def create_new_subject(request):
	subjectcreatefrom = SubjectCreateFrom()
	if request.method == 'POST':
		subjectcreatefrom = SubjectCreateFrom(request.POST)
		if subjectcreatefrom.is_valid():
			edit_subjectcreatefrom=subjectcreatefrom.save(commit=False)
			edit_subjectcreatefrom.hod=request.user
			edit_subjectcreatefrom.save()
			messages.success(request, f"Subject {edit_subjectcreatefrom.subject_name} has been created successfully")

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



