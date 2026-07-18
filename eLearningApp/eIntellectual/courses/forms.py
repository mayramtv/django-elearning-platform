from django import forms 

from .models import Course, Resource, ResourceType, Enrollment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code',
                  'name',
                  'category',
                  'teacher',
                  'date_created',
                  'description',
                  'image'
                  ]
        
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['code',
                  'course',
                  'content',
                  'text']
        
class ResourceTypeForm(forms.ModelForm):
    class Meta:
        model = ResourceType
        fields = ['resource_type']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student',
                  'course']
