# I write the following code following the following guidlines, documentation and classes
    # https://docs.djangoproject.com/en/5.1/
    # University of London Advance Web Development module
    # Lectures and Labs presented by Dr Daniel Buchan

from django.db import models
from management.models import User

from datetime import datetime  

# Teachers Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    account_number = models.CharField(max_length=100, blank=False, null=True)
    name = models.CharField(max_length=100, blank=False, null=True)
    last_name = models.CharField(max_length=100, blank=False, null=True)
    birthday = models.DateTimeField(blank=False, null=True)
    email = models.CharField(max_length=256, blank=False, null=True)
    user_name = models.CharField(max_length=100, blank=False, null=True)
    start_date = models.DateTimeField(default=datetime.now, blank=False, null=False)
    photo = models.ImageField(upload_to='teacher_images/', blank=True, null=True)

    def __str__(self): 
        return self.name 


# TeacherStatus: each teacher can show in their home page their status
class TeacherStatus(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    content = models.CharField(max_length=100, blank=False, null=True)