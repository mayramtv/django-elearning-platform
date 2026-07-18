# import models
from django.contrib import admin
from .models import Teacher, TeacherStatus

admin.site.register(Teacher) 
admin.site.register(TeacherStatus) 