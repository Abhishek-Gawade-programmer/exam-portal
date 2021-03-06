from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist


from .models import *
from django.middleware.csrf import get_token
from django.utils import timezone
import json
from django.http import HttpResponseRedirect
import base64

#MULTIPLE AUTHENTICATION 
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from .forms import StudentSignUpForm,TeacherSignUpForm

from django.contrib.auth import logout


from django.contrib import messages


from datetime import datetime, timedelta













class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'student_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('student_dashboard')

    

        
class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'teacher_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        # return redirect('students:quiz_list')
        return redirect("student_dashboard") 

@login_required
def redirect_after_login(request):
    if request.user.is_student:
        return redirect("student_dashboard") 
    elif request.user.is_teacher:
        return redirect("my_subject")
    elif request.user.is_hod:
        
        return redirect("all_subject") 
    else:
        logout(request)
        messages.error(request, f"Your login with different account please login  with correct account")
        return redirect('login')


def allow_to_students(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_student:
                current_student=Student.objects.get(user=request.user)
                if current_student.verify:
                    return view_func(request,*args, **kwargs)
                else:
                    messages.error(request, f"Your account is not verify yet please contact the teacher for verfication")
                    return redirect('login')

            else:
                messages.error(request, f"Your login with different account please login  with correct account")
                return redirect('login')

    return wrapper_func

@login_required
@allow_to_students
def student_dashboard(request):
    current_student=Student.objects.get(user=request.user)
    all_subject=current_student.student_subjects.all()
    reports_student=ReportStudent.objects.filter(student=current_student.user)
    return render(request,'students/student_dashboard.html',{
        'all_subject':all_subject,
        'reports_student':reports_student
        })


@login_required
@allow_to_students
def student_subject_detail(request,pk):
    current_student=Student.objects.get(user=request.user)
    subject=Subject.objects.get(pk=pk)
    test_in_subject=Test.objects.filter(subject=subject,make_active=True)

    return render(request,'students/student_subject_deatils.html',{
        'subject':subject,
        'test_in_subject':test_in_subject,
        'current_student':current_student
        })




@login_required
@allow_to_students
def verification_of_student(request):
    if request.method=='POST' :
        current_test=Test.objects.get(id=int(request.POST.get('current_test')))
        from django.core.files.base import ContentFile
        data_img=request.POST.get('data_img')
        format, imgstr = data_img.split(';base64,') 
        ext = format.split('/')[-1] 
        data = ContentFile(base64.b64decode(imgstr),name=f'{request.user.get_full_name()}.' + ext )

        student_data=StudentExamCapture.objects.create(student=request.user,test=current_test,student_image=data)
        student_data.save()
        return JsonResponse({'success':'true'},safe=False)


@login_required
@allow_to_students
def taking_photo_of_student(request):
    if request.method=='POST' :
        current_test=Test.objects.get(id=int(request.POST.get('current_test')))
        from django.core.files.base import ContentFile
        data_img=request.POST.get('data_img')
        format, imgstr = data_img.split(';base64,') 
        ext = format.split('/')[-1] 
        data = ContentFile(base64.b64decode(imgstr),name=f'{request.user.get_full_name()}.' + ext )

        student_data=StudentExamCapture.objects.create(student=request.user,test=current_test,student_image=data)
        student_data.save()
        return JsonResponse({'success':'true'},safe=False)



@login_required
@allow_to_students
def initial_setup(request,test_id):
    global current_test


    current_test=Test.objects.get(id=test_id)
    all_user_question=Question.objects.filter(test=current_test).order_by('?')[:current_test.total_question]
    #get the test
    check_test_given=UserQuestionList.objects.filter(test=current_test,student=request.user).exists()
    # print(check_test_given)


    if  not check_test_given:
        all_user_question_ids=[]    

        for each_question in all_user_question:
            if not StudentAnswer.objects.filter(question=each_question,test=current_test,student=request.user).exists():

                intial_student_answer=StudentAnswer.objects.create(question=each_question,test=current_test,student=request.user)
                intial_student_answer.save()

            if str(each_question.id) not in all_user_question_ids:
                all_user_question_ids.append(str(each_question.id))

        if not UserQuestionList.objects.filter(test=current_test,student=request.user).exists():

            student_test_data=UserQuestionList.objects.create(test=current_test,
                            student=request.user,test_question=json.dumps(all_user_question_ids),
                            start_time=timezone.now(),)

            
            duration=timedelta(hours=current_test.duration.hour,
                                 minutes=current_test.duration.minute,
                                 seconds=current_test.duration.second )
            if (timezone.now()+duration)>current_test.exam_end_time:
                student_test_data.end_time=current_test.exam_end_time
            else:
                student_test_data.end_time=timezone.now()+duration
            student_test_data.save()


            context={'time_left':student_test_data.end_time,'current_test':current_test}
            return render(request,'home.html',context)
    else:
        countiune_check_test_given=UserQuestionList.objects.get(test=current_test,student=request.user)

        if countiune_check_test_given.submit_time and not(current_test.allow_student_for_exam(request.user)):
            return render(request,'403_not_allowed.html')
        else:
            context={'time_left':countiune_check_test_given.end_time,'current_test':current_test}
            return render(request,'home.html',context)
@login_required
@allow_to_students
def save_question(request):
    if request.method=='POST' :
        question=get_object_or_404(Question,id=request.POST.get('pk'))
        student_answer=StudentAnswer.objects.get(question=question,test=current_test,student=request.user)
        student_answer.student_option=request.POST.get('option')
        student_answer.save()

        return JsonResponse({'success':'true'},safe=False)
    return JsonResponse({'success':'false'})





@login_required
@allow_to_students
def get_all_question_details(request):

    if request.method=='GET' :
        all_question_student=json.loads(UserQuestionList.objects.get(
                        student=request.user,test=current_test).test_question)

        all_question_json={}
        for i in range(len(all_question_student)):
            x=StudentAnswer.objects.get(student=request.user,question=all_question_student[i])
            all_question_json[i]={'seen':x.question_seen,'bookmark':x.bookmark,'student_option':x.student_option}


        return JsonResponse({'success':'true','all_question_json':all_question_json},safe=False)
    return JsonResponse({'success':'true','yes':'usidhb'},safe=False)


@login_required
@allow_to_students
def navigation_question(request):
    page_number=int(request.POST.get('page_number'))-1
    if page_number == len(Question.objects.all()):
        return JsonResponse({
            'success':'true',
            'next':'false'
            },safe=False)

    try :
        question_id=json.loads(UserQuestionList.objects.get(student=request.user,test=current_test).test_question)[page_number]
    except IndexError:
        return JsonResponse({'success':None},safe=False)

    question=get_object_or_404(Question,id=question_id)

    student_answer=StudentAnswer.objects.get(question=question,test=current_test,student=request.user)
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
        student_option= StudentAnswer.objects.get(question=question,test=question.test,student=request.user).student_option
        if student_option:
            data_for_new_question[f'option_{student_option}']['student_option']='checked'

    return JsonResponse(data_for_new_question,safe=False)



@login_required
@allow_to_students
def toogle_bookmark(request,page_number):
    page_number=page_number-1
    question_id=json.loads(UserQuestionList.objects.get(student=request.user,test=current_test).test_question)[page_number]
    question=get_object_or_404(Question,id=question_id)

    student_answer=StudentAnswer.objects.get(question=question,test=question.test,student=request.user)
    student_answer.question_seen=True

    if student_answer.bookmark:
        student_answer.bookmark=False
    else:
        student_answer.bookmark=True
        
    student_answer.save()


    toogle_bookmark={
        'success':'true',
        'done':student_answer.bookmark



        }

    return JsonResponse(toogle_bookmark,safe=False)
@login_required
@allow_to_students
def report_question(request,page_number,comment=''):
    page_number=page_number-1
    question_id=json.loads(UserQuestionList.objects.get(student=request.user,test=current_test).test_question)[page_number]
    question=get_object_or_404(Question,id=question_id)

    student_report_question=ReportQuestion.objects.filter(question=question,test=question.test,student=request.user)
    if student_report_question.exists():
        student_report_question=ReportQuestion.objects.get(question=question,test=question.test,student=request.user)
        student_report_question.comment=comment
    else:
        student_report_question=ReportQuestion.objects.create(question=question,test=question.test,student=request.user,comment=comment)
        
    student_report_question.save()


    report_succes={
        'success':'true',
        }

    return JsonResponse(report_succes,safe=False)


@login_required
@allow_to_students
def submit_exam(request):
    question_id=json.loads(UserQuestionList.objects.get(student=request.user,test=current_test).test_question)[0]
    question=get_object_or_404(Question,id=question_id)
    x=UserQuestionList.objects.get(test=current_test,student=request.user)
    x.submit_time=timezone.now()
    x.save()
    tick_question=StudentAnswer.objects.filter(student=request.user,test=question.test).exclude(student_option='').count()

    return render(request,'exam_submit.html',{'exam_info':x,'tick_question':tick_question})


@allow_to_students
@login_required
def student_result(request, test_id,student_id):

    current_student = get_object_or_404(Student, pk = student_id)
    current_test= get_object_or_404(Test, pk = test_id)
    try :
        student_questions=UserQuestionList.objects.get(student=current_student.user,test=current_test)
    except ObjectDoesNotExist:
        messages.error(request, f"You Have not given exam yet !!")
        return redirect("student_subject_detail",pk=current_test.subject.pk)

    student_questions_with_sr=json.loads(student_questions.test_question)
    all_student_questions_with_sr=[]  
    for student_question in student_questions_with_sr:
        question= get_object_or_404(Question, id = student_question)
        all_student_questions_with_sr.append(
                            StudentAnswer.objects.get(
                            question=question,
                            student=current_student.user,test=current_test
                            ))
    score=f'{student_questions.number_of_correct_answers()}/{current_test.total_question}'
    result=True if student_questions.number_of_correct_answers()>current_test.passing_marks else False

    return render(request, "students/student_result.html", {
                            'all_student_questions':all_student_questions_with_sr,'score':score,
                            'current_student':current_student,
                            'current_test':current_test,
                            'result':result})







































