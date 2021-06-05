from django import forms
from students.models import *




class TestCreateFrom(forms.ModelForm):
    class Meta:
        model=Test
        fields ='__all__'
        exclude=('teacher','subject')

        widgets = {

            # 'verify_order': forms.CheckboxInput(attrs={'class':"form-check-input", 'type':"checkbox", 'id':"checkbox1"}),
            # 'delivered': forms.CheckboxInput(attrs={'class':"form-check-input", 'type':"checkbox", 'id':"checkbox2",}),
            # 'payment_done': forms.CheckboxInput(attrs={'class':"form-check-input", 'type':"checkbox", 'id':"checkbox3"}),



        }



class SubjectCreateFrom(forms.ModelForm):
    class Meta:
        model=Subject
        exclude=('hod',)

        widgets = {

            # 'verify_order': forms.CheckboxInput(attrs={'class':"form-check-input", 'type':"checkbox", 'id':"checkbox1"}),
            # 'delivered': forms.CheckboxInput(attrs={'class':"form-check-input", 'type':"checkbox", 'id':"checkbox2",}),
            # 'payment_done': forms.CheckboxInput(attrs={'class':"form-check-input", 'type':"checkbox", 'id':"checkbox3"}),



        }