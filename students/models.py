from django.db import models
import uuid
from django.utils import timezone
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import json
CORRECT_ANSWER =(
    ('1','Option 1'),
    ('2','Option 2'),
    ('3','Option 3'),
    ('4','Option 4'),
)



class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    def __str__(self):
        return  str(self.get_full_name())





class Subject(models.Model):
    hod=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    subject_name=models.CharField(max_length=300,unique=True,help_text = "Enter Subject Name <b>Do Not Duplicate </b>",)
    subject_code=models.CharField(max_length=10,unique=True,help_text = "Enter Subject Code <b>Given by SPPU</b>",)
    teachers=models.ManyToManyField(User,related_name='subject_teachers',
                            help_text = "Use <b>control + arrow</b> click to select multiple teachers",
                            verbose_name='Select Teachers Want To Include')
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


    def no_of_test_in_subject(self):
        return Test.objects.filter(subject=self,make_active=True).count()

    def __str__(self):
        return self.subject_name


class Test(models.Model):
    teacher=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    test_title =models.CharField(max_length=300,help_text = "Title For Your test <b>Not Subject Name</b>")
    exam_start_time=models.DateTimeField(help_text = " <em> YYYY-MM-DD HH-MM-SS (in 24hrs)</em>.")
    exam_end_time=models.DateTimeField(help_text = " <em> YYYY-MM-DD HH-MM-SS (in 24hrs)</em>.")

    duration=models.TimeField(default='01:00:00',help_text = "Please use the following format: <em>HH-MM-SS</em>.")
    make_active=models.BooleanField(default=False,help_text = "Make Exam Active Please Be aware of it!!")
    total_question=models.IntegerField(default=0,help_text = "Total Questions You Created")
    max_mark=models.IntegerField(default=0,help_text = "Max marks of this Test")
    passing_marks=models.IntegerField(default=0,
        help_text = "Keep Zero for <b>No Passing Criteria </b> and Less than <b>Max</b> marks")
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    show_result=models.BooleanField(default=False)
    
    def __str__(self):
        return self.test_title+ str(self.duration)

    def allow_student_for_exam(self,student):
        time=timezone.now()

        if (time>self.exam_start_time) and (time<self.exam_end_time):
            print('sdfgs')
            if UserQuestionList.objects.filter(student=student,test=self).exists():
                test_for_student=UserQuestionList.objects.get(student=student,test=self)
                if timezone.now() > test_for_student.end_time:
                    return False
                elif (not test_for_student.submit_time) and (test_for_student.start_time  < time)  :
                    return True
                else:
                    return False
            return True
        else:
            return False

    def get_total_questions(self):
        return Question.objects.filter(test=self).count()


class Question(models.Model):
    id=models.UUIDField(primary_key=True,
                    default=uuid.uuid4,
                    editable=False,
                    db_index=True,)

    teacher=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    question_title =models.TextField(max_length=3000,unique=True,
                help_text='make sure question should me <b>Clear and Not Duplicate</b>')
    option_1=models.CharField(max_length=200,help_text='Option 1 should not to be repeat')
    option_2=models.CharField(max_length=200,help_text='Option 2 should not to be repeat')
    option_3=models.CharField(max_length=200,help_text='Option 3 should not to be repeat')
    option_4=models.CharField(max_length=200,help_text='Option 4 should not to be repeat')
    # question_marks=models.FloatField(default=1,help_text='Marks for this question <b>Default is 1.0</b>')
    test= models.ForeignKey(Test,on_delete=models.CASCADE)
    correct_option = models.CharField(choices=CORRECT_ANSWER,verbose_name='Correct Option',max_length=1,default='')
    created =models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.question_title



class StudentAnswer(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    question= models.ForeignKey(Question,on_delete=models.SET_NULL,blank=True,null=True)
    test= models.ForeignKey(Test,on_delete=models.SET_NULL,blank=True,null=True)
    question_seen=models.BooleanField(default=False)
    bookmark=models.BooleanField(default=False)
    student_option = models.CharField(choices=CORRECT_ANSWER,verbose_name="Student's Option",
                max_length=1,default='',blank=True,null=True)
    def __str__(self):
        return  f'{self.question.question_title}--'+str(self.student_option)

    

class ReportQuestion(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    question= models.ForeignKey(Question,on_delete=models.SET_NULL,blank=True,null=True)
    test= models.ForeignKey(Test,on_delete=models.SET_NULL,blank=True,null=True)
    comment=models.CharField(max_length=200,verbose_name='Comment For Spam')


class UserQuestionList(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    test= models.ForeignKey(Test,on_delete=models.SET_NULL,blank=True,null=True)
    start_time=models.DateTimeField()
    submit_time=models.DateTimeField(null=True,blank=True)
    end_time=models.DateTimeField(null=True)
    test_question=models.TextField(max_length=2000)

    def __str__(self):
        return f'{self.student}--{self.test}'




    def question_attempted(self):
        question_attempted_count=StudentAnswer.objects.filter(student=self.student,test=self.test
                                    ).exclude(student_option=None).count()
        return question_attempted_count

    def student_exam_time_left(self):
        return self.end_time-timezone.now()





    def number_of_correct_answers(self):
        all_question_attempted=StudentAnswer.objects.filter(student=self.student,test=self.test
                                    ).exclude(student_option=None)
        correct_answer=0
        for student_answer in all_question_attempted:
            if student_answer.student_option==student_answer.question.correct_option:
                correct_answer+=1

            # print(student_answer.question.student_option)
        return correct_answer


class StudentExamCapture(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    test= models.ForeignKey(Test,on_delete=models.SET_NULL,blank=True,null=True)
    student_image=models.ImageField(blank=True)
    created =models.DateTimeField(auto_now_add=True)
   




class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    teacher_subjects = models.ManyToManyField(Subject,related_name='teacher_subjects')
    phone_number=models.CharField(max_length=20)
    class_teacher_roll =models.CharField(max_length=10,)
    verify=models.BooleanField(default=False)



    def save(self, *args, **kwargs):
        self.class_teacher_roll = self.class_teacher_roll.upper()
        super().save(*args, **kwargs)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_subjects = models.ManyToManyField(Subject,related_name='student_subjects')
    college_rollno =models.CharField(max_length=10,unique=True,error_messages={
                'unique':"This rollno has already been registered."})
    phone_number=models.CharField(max_length=20)
    verify=models.BooleanField(default=False)

    def get_all_given_test_details(self):
        return UserQuestionList.objects.filter(student=self.user,test__make_active=True)
    
    def save(self, *args, **kwargs):
        self.college_rollno = self.college_rollno.upper()
        super().save(*args, **kwargs)








