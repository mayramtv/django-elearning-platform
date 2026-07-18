
from django import forms 
from django.contrib.auth.forms import UserCreationForm

from management.models import User
from .models import Student, StudentStatus

# Create a form for user and password
class StudentForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

# creates a form for the user details
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['account_number', 
                  'name', 
                  'last_name', 
                  'birthday', 
                  'email', 
                  'start_date', 
                  'photo']

# creates a form for the user status
class StudentStatusForm(forms.ModelForm):
    class Meta:
        model = StudentStatus
        fields = ['content']
 
    