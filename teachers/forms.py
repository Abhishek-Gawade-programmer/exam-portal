from django import forms
from students.models import *
from django.utils import timezone



class TestCreateFrom(forms.ModelForm):
    class Meta:
        model=Test
        fields ='__all__'
        exclude=('teacher','subject')

        widgets = {

        }

    def clean_make_active(self):
        make_active = self.cleaned_data['make_active']
        exam_start_time = self.cleaned_data['exam_start_time']
        now=timezone.now()
        print(make_active,exam_start_time,timezone.now(),timezone.now() < exam_start_time,)
        if timezone.now() > exam_start_time:
            raise forms.ValidationError("you can't change the active as exam is already start")
        return make_active




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