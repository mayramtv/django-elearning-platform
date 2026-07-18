# import models
from django.contrib import admin
from .models import Student, StudentStatus

admin.site.register(Student) 
admin.site.register(StudentStatus) 