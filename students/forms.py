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

    college_rollno = forms.CharField(max_length=100,
    	widget=forms.TextInput,
    	required=True)

    phone_number = forms.CharField(max_length=10,
    	widget=forms.NumberInput)



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
        teacher.save()
        return user