from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import json
CORRECT_ANSWER =(
    ('1','Option 1'),
    ('2','Option 2'),
    ('3','Option 3'),
    ('4','Option 4'),
)



class Subject(models.Model):
    hod=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    subject_name=models.CharField(max_length=300,unique=True,help_text = "Enter Subject Name <b>Do Not Duplicate </b>",)
    teachers=models.ManyToManyField(User,related_name='subject_teachers',help_text = "Use <b>control + arrow</b> click to select multiple teachers",verbose_name='Select Teachers Want To Include')
    

    def __str__(self):
        return self.subject_name


class Test(models.Model):
    teacher=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    test_title =models.CharField(max_length=300,unique=True,help_text = "Title For Your test <b>Not Subject Name</b>")
    duration=models.TimeField(default='01:00:00',help_text = "Please use the following format: <em>HH-MM-SS</em>.")
    make_active=models.BooleanField(default=False,help_text = "Make Exam Active Please Be aware of it!!")
    total_question=models.IntegerField(default=0,help_text = "Total Questions You Created")
    max_mark=models.IntegerField(default=0,help_text = "Max marks of this Test")
    passing_marks=models.IntegerField(default=0,help_text = "Keep Zero for <b>No Passing Criteria </b> and Less than <b>Max</b> marks")
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)


    def __str__(self):
        return self.test_title+ str(self.duration)

class Question(models.Model):
    id=models.UUIDField(primary_key=True,
                    default=uuid.uuid4,
                    editable=False,
                    db_index=True,)

    teacher=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    question_title =models.CharField(max_length=300,unique=True,)
    option_1=models.CharField(max_length=200)
    option_2=models.CharField(max_length=200)
    option_3=models.CharField(max_length=200)
    option_4=models.CharField(max_length=200)
    question_marks=models.FloatField(default=1)
    test= models.ForeignKey(Test,on_delete=models.CASCADE)
    correct_option = models.CharField(choices=CORRECT_ANSWER,verbose_name='Correct Option',max_length=1,default='1')

    def __str__(self):
        return self.question_title



class StudentAnswer(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    question= models.ForeignKey(Question,on_delete=models.SET_NULL,blank=True,null=True)
    test= models.ForeignKey(Test,on_delete=models.SET_NULL,blank=True,null=True)
    question_seen=models.BooleanField(default=False)
    bookmark=models.BooleanField(default=False)
    student_option = models.CharField(choices=CORRECT_ANSWER,verbose_name="Student's Option",max_length=1,default='',blank=True,null=True)
    def __str__(self):
        return self.question.question_title+ str(self.student_option)

    

class ReportQuestion(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    question= models.ForeignKey(Question,on_delete=models.SET_NULL,blank=True,null=True)
    test= models.ForeignKey(Test,on_delete=models.SET_NULL,blank=True,null=True)
    comment=models.CharField(max_length=200,verbose_name='Comment For Spam')


class UserQuestionList(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,default=False,null=True)
    test= models.ForeignKey(Test,on_delete=models.SET_NULL,blank=True,null=True)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField(null=True)
    test_question=models.TextField(max_length=2000)













