# I write the following code following the following guidlines, documentation and classes
    # https://docs.djangoproject.com/en/5.1/
    # University of London Advance Web Development module
    # Lectures and Labs presented by Dr Daniel Buchan

from django.db import models
from datetime import datetime  
from teachers.models import Teacher
from students.models import Student

# Course Model
class Course(models.Model):
    code = models.CharField(max_length=100, blank=False, null=True)
    name = models.CharField(max_length=100, blank=False, null=True)
    category = models.CharField(max_length=100, blank=False, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(default=datetime.now, blank=False, null=True)
    date_updated = models.DateTimeField(auto_now=True, blank=False, null=True)
    description = models.CharField(max_length=100, blank=False, null=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self): 
        return self.code 
    

# Resource Models: each course contain resources 
class Resource(models.Model):
    code = models.CharField(max_length=100, blank=False, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    content = models.FileField(upload_to='resources_files/', blank=True, null=True)
    text = models.TextField(blank=True, null=True)

# ResorceType: states the type of the resource updated
class ResourceType(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True)
    resource_type = models.CharField(max_length=100, blank=False, null=True)

# Enrollment: each student can be enrolled in a courses 
class Enrollment(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    course =  models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
