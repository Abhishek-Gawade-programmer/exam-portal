from django.db import models
import uuid
from django.contrib.auth import get_user_model


CORRECT_ANSWER =(
    ('1','Option 1'),
    ('2','Option 2'),
    ('3','Option 3'),
    ('4','Option 4'),
)






class Subject(models.Model):
    subject_name=models.CharField(max_length=300)
    

    def __str__(self):
        return self.subject_name


class Test(models.Model):
    test_title =models.CharField(max_length=300)

    start_time=models.DateTimeField()

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    max_mark=models.IntegerField(default=0)
    passing_marks=models.IntegerField(default=0)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)


    @property
    def duration(self):
        return self.end_time - self.start_time
    

    def __str__(self):
        return self.test_title+ str(self.duration)

class Question(models.Model):
    id=models.UUIDField(primary_key=True,
                    default=uuid.uuid4,
                    editable=False,
                    db_index=True,)

    question_title =models.CharField(max_length=300)
    option_1=models.CharField(max_length=200)
    option_2=models.CharField(max_length=200)
    option_3=models.CharField(max_length=200)
    option_4=models.CharField(max_length=200)
    test= models.ForeignKey(Test,on_delete=models.CASCADE)
    correct_option = models.CharField(choices=CORRECT_ANSWER,verbose_name='Correct Option',max_length=1,default='1')

    def __str__(self):
        return self.question_title



class StudentAnswer(models.Model):
    #user
    question= models.ForeignKey(Question,on_delete=models.SET_NULL,blank=True,null=True)
    test= models.ForeignKey(Test,on_delete=models.SET_NULL,blank=True,null=True)
    correct_option = models.CharField(choices=CORRECT_ANSWER,verbose_name="Student's Option",max_length=1,blank=True,null=True)


    def __str__(self):
        return self.question.question_title+ str(self.correct_option)









