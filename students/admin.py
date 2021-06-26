from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
# admin.site.register(User)

admin.site.register(ReportQuestion)
admin.site.register(UserQuestionList)

admin.site.register(Subject)
admin.site.register(Test)

admin.site.register(Question)
admin.site.register(StudentAnswer)
admin.site.register(StudentExamCapture)

