from django import forms

from .models import *

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction









class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='First Name',widget=forms.TextInput,required=True)
    last_name = forms.CharField(max_length=30, label='Last Name',widget=forms.TextInput,required=True)
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={"type": "email",}))

    student_subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    college_rollno = forms.CharField(max_length=100,label='Collage Roll Number',
    	widget=forms.NumberInput,
    	required=True,help_text = "Only Collage <b>Number </b>",)

    phone_number = forms.CharField(max_length=10,
    	widget=forms.NumberInput)

    def clean_college_rollno(self):
        college_rollno ='FECOMPD'+self.cleaned_data['college_rollno']
        if Student.objects.filter(college_rollno=college_rollno).exists():
            raise forms.ValidationError("rollno already exists")
        return college_rollno



    class Meta(UserCreationForm.Meta):
        model = User


    @transaction.atomic
    def save(self):
        
        user = super().save(commit=False)
        user.is_student = True
        user.first_name=self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('last_name')
        user.email=self.cleaned_data.get('email')
        user.save()
        student = Student.objects.create(user=user)
        student.college_rollno=self.cleaned_data.get('college_rollno')
        student.phone_number=self.cleaned_data.get('phone_number')

        student.save()
        return user


class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='First Name',widget=forms.TextInput,required=True)
    last_name = forms.CharField(max_length=30, label='Last Name',widget=forms.TextInput,required=True)
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={"type": "email",}))

    teacher_subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    phone_number = forms.CharField(max_length=10,
        widget=forms.NumberInput)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        
        user.first_name=self.cleaned_data.get('first_name')
        user.last_name=self.cleaned_data.get('last_name')
        user.email=self.cleaned_data.get('email')
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.phone_number=self.cleaned_data.get('phone_number')
        teacher.class_teacher_roll='FECOMPD'
        for _ in self.cleaned_data.get('teacher_subjects'):
            _.teachers.add(user)
            teacher.teacher_subjects.add(_)
        teacher.save()
        return user