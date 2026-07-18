# import models
from django.contrib import admin
from .models import Course, Resource, ResourceType, Enrollment

admin.site.register(Course) 
admin.site.register(Resource) 
admin.site.register(ResourceType) 
admin.site.register(Enrollment) 