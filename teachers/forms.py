from django import forms
from students.models import *




class TestCreateFrom(forms.ModelForm):
    class Meta:
        model=Test
        fields ='__all__'
        exclude=('teacher','subject')

        widgets = {

        }



class SubjectCreateFrom(forms.ModelForm):
    class Meta:
        model=Subject
        exclude=('hod',)

        widgets = {


        }


class QuestionCreateFrom(forms.ModelForm):
    class Meta:
        model=Question
        exclude=('teacher','test')

        widgets = {

        }


class StudentVerificationFrom(forms.ModelForm):
    class Meta:
        model=Student
        exclude=('user','verify')

        widgets = {

        }