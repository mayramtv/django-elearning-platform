from django import forms 
from django.contrib.auth.forms import UserCreationForm

from management.models import User
from .models import Teacher, TeacherStatus

# Create a form for user and password
class TeacherForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

# creates a form for the user details
class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['account_number', 
                  'name', 
                  'last_name', 
                  'birthday', 
                  'email', 
                  'start_date', 
                  'photo']

# creates a form for the user status
class TeacherStatusForm(forms.ModelForm):
    class Meta:
        model = TeacherStatus
        fields = ['content']
        
    
