from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from students.models import *
from django.utils import timezone
import json
from django.views.generic import ListView,DetailView,View,CreateView,UpdateView

from .forms import (TestCreateFrom,SubjectCreateFrom,
						QuestionCreateFrom,StudentVerificationFrom,
						TeacherVerificationFrom)
from django.contrib import messages

from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required




def allow_to_hod(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_hod:
            	return view_func(request,*args, **kwargs)
            else:
            	messages.success(request, f"Your authorized to access this page. Would you like to login to a different account?")
            	return redirect("login")
        else:
        	return redirect("login")

    return wrapper_func



def allow_to_teacher_hod(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            if (request.user.is_teacher) or request.user.is_hod:
            	if request.user.is_hod:
            		return view_func(request,*args, **kwargs)
            	else:
            		if get_object_or_404(Teacher, user = request.user).verify:
            			return view_func(request,*args, **kwargs)
            		else:
                		messages.error(request, f"Your account is not verified please contact the HOD for same")
                		return redirect("login")
            else:
            	messages.success(request, f"Your authorized to access this page. Would you like to login to a different account?")
            	return redirect("login")
        else:
         	return redirect("login")

    return wrapper_func


@allow_to_teacher_hod
@login_required
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

	return render(request,'teachers/create_new_test.html',
		{'testcreatefrom':testcreatefrom})


@allow_to_hod
@login_required
# @allow_to_hod
def create_new_subject(request):
	subjectcreatefrom = SubjectCreateFrom()
	if request.method == 'POST':
		subjectcreatefrom = SubjectCreateFrom(request.POST)
		if subjectcreatefrom.is_valid():
			edit_subjectcreatefrom=subjectcreatefrom.save(commit=False)
			edit_subjectcreatefrom.hod=request.user
			# edit_subjectcreatefrom.teachers.clear()
			edit_subjectcreatefrom.save()
			subject_object = get_object_or_404(Subject, pk = edit_subjectcreatefrom.pk)
			for _ in subjectcreatefrom.cleaned_data['teachers']:
				subject_object.teachers.add(_)
			subject_object.save()
			messages.success(request, f"New Subject :: {edit_subjectcreatefrom.subject_name} has been created successfully")
			return redirect("all_subject")

	return render(request,'teachers/create_new_subject.html',{'subjectcreatefrom':SubjectCreateFrom})



@allow_to_teacher_hod
@login_required
def subject_list_view(request):
    all_subject=Subject.objects.filter(teachers__in=[request.user,])
    return render(request,'teachers/all_subject_list.html',
    			{'all_subject':all_subject})

# def show():
# 	pass



@allow_to_hod
@login_required
def for_hod_subject_list_view(request):
    all_subject=Subject.objects.all()
    return render(request,'teachers/all_subject_list.html',
    			{'all_subject':all_subject})

@allow_to_teacher_hod
@login_required
def subject_detail_view(request,pk):
    subject=Subject.objects.get(pk=pk)
    test_in_subject=Test.objects.filter(subject=subject)
    return render(request,'teachers/subject_detail.html',
    			{'subject':subject,'test_in_subject':test_in_subject})

@allow_to_teacher_hod
@login_required
def test_detail_view(request,pk):
    test=Test.objects.get(pk=pk)
    ques_in_test=Question.objects.filter(test=test)
    return render(request,'teachers/test_detail.html',
    			{'test':test,'ques_in_test':ques_in_test})
@allow_to_hod
@login_required
def subject_update_view(request, pk):
 
    subject_object = get_object_or_404(Subject, pk = pk)
 
    subject_update_form = SubjectCreateFrom(request.POST or None, 
    	instance = subject_object)

    if subject_update_form.is_valid():
    	edit_subject_update_form=subject_update_form.save(commit=False)
    	edit_subject_update_form.hod=request.user
    	edit_subject_update_form.teachers.clear()
    	for _ in subject_update_form.cleaned_data['teachers']:
    		subject_object.teachers.add(_)
    	subject_object.save()
    	edit_subject_update_form.save()
    	messages.info(request, f"{edit_subject_update_form.subject_name} has been Updated successfully !!")
    	return redirect("all_subject")

 
    return render(request, "teachers/subject_update_form.html", {
    			'subject_update_form':subject_update_form,
    			'subject':subject_object})

@allow_to_teacher_hod
@login_required
def create_new_question(request,test_id,add_another=False):
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
			if not add_another:
				return redirect("test_detail",pk=test.id)
			else:
				return redirect("question_create",test_id=test.id)

	return render(request,'teachers/create_new_question.html',{'questioncreatefrom':questioncreatefrom,'test':test})



@allow_to_teacher_hod
@login_required
def test_update_view(request, pk):
 
    test_object = get_object_or_404(Test, id = pk)
 
    test_update_form = TestCreateFrom(request.POST or None, instance = test_object)
    test_active_status=test_object.make_active
    test_start_time=test_object.exam_start_time
    test_end_time=test_object.exam_end_time
    if test_update_form.is_valid():
    	edit_test_update_form=test_update_form.save(commit=False)

    	if  (edit_test_update_form.exam_end_time < edit_test_update_form.exam_start_time):
    		messages.error(request, f"make sure dates times of start exam and end exam are correct")
    		return redirect("test_update",pk=test_object.subject.id)
    	elif  (edit_test_update_form.make_active) and (test_object.get_total_questions()<edit_test_update_form.total_question):
    		messages.error(request, f"Yon can't MAKE ACTIVE as number of questions not SATISFIED")
    		return redirect("test_update",pk=test_object.subject.id)



    	edit_test_update_form.subject=test_object.subject
    	edit_test_update_form.teacher=request.user
    	edit_test_update_form.save()
    	messages.success(request, f"{test_object.test_title} has been Updated successfully !!")
    	return redirect("test_detail",pk=test_object.id)

 
    return render(request, "teachers/test_update_form.html", {
    			'test_update_form':test_update_form,'test':test_object})

@allow_to_teacher_hod
@login_required
def question_update_view(request, pk):
 
    question_object = get_object_or_404(Question, id = pk)
 
    question_update_form = QuestionCreateFrom(request.POST or None, 
    	instance = question_object)

    if question_update_form.is_valid():
    	edit_question_update_form=question_update_form.save(commit=False)
    	edit_question_update_form.teacher=request.user
    	edit_question_update_form.test=question_object.test
    	edit_question_update_form.save()
    	messages.success(request, f"{question_object.question_title} has been Updated successfully !!")
    	return redirect("test_detail",pk=question_object.test.id)

 
    return render(request, "teachers/question_update_form.html", {
    			'question_update_form':question_update_form,'question':question_object})



@allow_to_teacher_hod
@login_required
def show_all_student(request):
	if request.user.is_teacher :
		current_teacher=Teacher.objects.get(user=request.user)
		my_students=Student.objects.filter(college_rollno__icontains=current_teacher.class_teacher_roll)
	elif request.user.is_hod:
		current_teacher=Teacher.objects.get(user=request.user)
		my_students=Student.objects.all()

	return render(request, "teachers/my_students.html", {
    			'my_students':my_students})

@allow_to_teacher_hod
@login_required
def verify_the_student(request,pk):

	current_student=get_object_or_404(Student, pk = pk)
	if current_student.verify:
		current_student.verify=False
		messages.error(request, f" Roll No:{current_student.college_rollno} has been Unverified successfully !!")
	else:
		current_student.verify=True
		messages.success(request, f" Roll No:{current_student.college_rollno} has been Verified successfully !!")
	current_student.save()
	#email to student that verification is done
	return redirect("my_students")


@allow_to_teacher_hod
@login_required
def student_update_view(request, pk):
 
    current_student=get_object_or_404(Student, pk = pk)
 
    student_verfiy_form = StudentVerificationFrom(request.POST or None, instance = current_student)

    if student_verfiy_form.is_valid():
    	print(student_verfiy_form.cleaned_data,student_verfiy_form.cleaned_data['student_subjects'][0])
    	edit_student_verfiy_form=student_verfiy_form.save(commit=False)
    	current_student.student_subjects.clear()
    	for _ in student_verfiy_form.cleaned_data['student_subjects']:
    		current_student.student_subjects.add(_)
    	current_student.save()
    	edit_student_verfiy_form.save()
    	messages.success(request, f"{edit_student_verfiy_form.college_rollno} has been Updated successfully !!")
    	return redirect("my_students")
    	# return redirect("subject_detail",pk=test_object.subject.id)

 
    return render(request, "teachers/student_update_form.html", {
    			'student_verfiy_form':student_verfiy_form,'current_student':current_student})


@allow_to_teacher_hod
@login_required
def delete_the_question(request, pk):
    question_object = get_object_or_404(Question, id = pk)
    messages.error(request, f"{question_object.question_title} has been Delete successfully !!")
    test=question_object.test
    question_object.delete()
    question_object.save()
    return redirect("test_detail",pk=test.id)


@allow_to_teacher_hod
@login_required
def student_all_test_detail(request, pk):
    current_student = get_object_or_404(Student, pk = pk)
    test_given_by_student=current_student.get_all_given_test_details()
    return render(request, "teachers/test_given_by_student.html", {
    			'test_given_by_student':test_given_by_student,
    			'current_student':current_student})


@allow_to_teacher_hod
@login_required
def student_exam_result(request, test_id,student_id):

    current_student = get_object_or_404(Student, pk = student_id)
    current_test= get_object_or_404(Test, pk = test_id)
    student_questions=UserQuestionList.objects.get(student=current_student.user,test=current_test)
    student_questions_with_sr=json.loads(student_questions.test_question)
    all_student_questions_with_sr=[]  

    all_pictures=StudentExamCapture.objects.filter(student=current_student.user,test=current_test)
    for student_question in student_questions_with_sr:
    	question= get_object_or_404(Question, id = student_question)
    	all_student_questions_with_sr.append(
	    					StudentAnswer.objects.get(
	    					question=question,
	    					student=current_student.user,test=current_test
    						))
    score=f'{student_questions.number_of_correct_answers()}/{current_test.total_question}'
    result=True if student_questions.number_of_correct_answers()>current_test.passing_marks else False
    return render(request, "teachers/test_result_of_student.html", {
    					'current_student':current_student,
    					'all_student_questions':all_student_questions_with_sr,
    					'score':score,
    					'all_pictures':all_pictures})


@allow_to_hod
@login_required
def all_teacher_details(request):
    all_teacher=Teacher.objects.all()
    return render(request,'teachers/all_teacher_list.html',
    			{'all_teacher':all_teacher})


@allow_to_hod
@login_required
def verify_the_teacher(request,pk):

	current_teacher=get_object_or_404(Teacher, pk = pk)
	if current_teacher.verify:
		current_teacher.verify=False
		messages.error(request, f"{current_teacher.user.get_full_name()} of :{current_teacher.class_teacher_roll} has been Unverified successfully !!")
	else:
		current_teacher.verify=True
		messages.success(request, f" {current_teacher.user.get_full_name()}:of {current_teacher.class_teacher_roll} has been Verified successfully !!")
	current_teacher.save()
	#email to student that verification is done
	return redirect("all_teacher_details")


@allow_to_hod
@login_required
def teacher_update_view(request, pk):
 
    current_teacher=get_object_or_404(Teacher, pk = pk)
 
    teacher_verfiy_form = TeacherVerificationFrom(request.POST or None, instance = current_teacher)

    if teacher_verfiy_form.is_valid():
    	edit_teacher_verfiy_form=teacher_verfiy_form.save(commit=False)
    	current_teacher.teacher_subjects.clear()
    	for _ in teacher_verfiy_form.cleaned_data['teacher_subjects']:
    		
    		current_teacher.teacher_subjects.add(_)
    	current_teacher.save()
    	edit_teacher_verfiy_form.save()
    	messages.success(request, f" {current_teacher.user.get_full_name()}:of {current_teacher.class_teacher_roll} has been Updated  successfully !!")
    	return redirect("all_teacher_details")

 
    return render(request, "teachers/teacher_update_form.html", {
    			'teacher_verfiy_form':teacher_verfiy_form,'current_teacher':current_teacher})





def report_student_test(request,test_id,student_id):
    current_student = get_object_or_404(Student, pk = student_id)
    current_test= get_object_or_404(Test, pk = test_id)


def demo_login(request,student=None,teacher=None,hod=None):
	if student:
		user =authenticate(request,
				username='demo_student',
				password='w8Q7kVdwvKcs7J2')
	elif teacher:
		print('asjebhjfsebhb')
		user =authenticate(request,
			username='demo_teacher',
			password='758qccCN7GkBNBG')

	elif hod:
		user =authenticate(request,
			username='hod',
			password='hod123@#')

	login(request, user)
	return redirect("redirect_after_login") 
