from django import template
from  students.models import Test

register = template.Library()
@register.filter
def eligible_student_test(student,test_id,):
    if student.is_authenticated:
        test_for_student=Test.objects.get(pk=test_id)
        return test_for_student.allow_student_for_exam(student=student)


# @register.filter
# def get_str_na_a(short_str):
# 	if short_str == ''


