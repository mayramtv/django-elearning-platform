from typing import Any
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView 

from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy


from .models import Course, Resource, ResourceType
from students.models import Student
from teachers.models import Teacher
from management.models import User
from .forms import *

from management.views import base_template_data, base_data

@login_required()
def create_course(request):
    created = False
    # get data for base.html template
    context = {}
    context = base_data(context)

    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES)

        # validate form data
        if course_form.is_valid():
            # save user and profile form  data
            course = course_form.save()
            course.save()
            created = True

            context['course_form'] = course_form
            context['course'] = course
            context['created'] = created
            # passes content for base template,  courses, and form
            return render(request, 'courses/create_course.html', context)
    else:
        teacher = Teacher.objects.get(user__pk=request.user.pk)
        init_data = {'teacher': teacher}
        course_form = CourseForm(initial=init_data)
    
    context['course_form'] = course_form
    context['created'] = created
    # passes content for base template, and form
    return render(request, 'courses/create_course.html', context)

class CourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy('teacher:classroom')

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        # get data for base.html template
        context = base_data(context)

        return context 


class CourseDetail(DetailView):
    model = Course
    template_name = 'courses/course.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        owns_course = False
        enrollment_exist = False

        resources_group = Resource.objects.filter(course=kwargs['object'])
        resources = [(resource, ResourceType.objects.get(resource=resource).resource_type) for resource in resources_group]
        context['resources'] = resources

        # gets object being used 
        try:
            course = Course.objects.get(pk=kwargs['object'].pk)
        except Course.DoesNotExist:
            return HttpResponse(status=404)

        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                student = Student.objects.get(user__pk=self.request.user.pk)
                enrollment_exist = student_course_enrollment(student, course)
                if enrollment_exist:
                    enrollment = Enrollment.objects.filter(student__pk=student.pk).get(course__pk=course.pk)
                    context['enrollment'] = enrollment
            elif self.request.user.is_teacher:
                teacher = Teacher.objects.get(user__pk=self.request.user.pk)
                classroom_courses = Course.objects.filter(teacher__pk=teacher.pk)
                if course in classroom_courses:
                    owns_course = True
                    enrollment_exist = False
            context['enrollment_exist'] = enrollment_exist
            context['owns_course'] = owns_course

        # get data for base.html template
        context = base_data(context)

        return context 

class CoursesList(ListView): 
    model = Course 
    template_name = 'courses/courses.html' 

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 

        # get courses 
        try:
            context['courses'] = Course.objects.all()
        except:
            context['courses']  = {}
            
        # get data for base.html template
        context = base_data(context)

        return context 
    

# @login_required
# @teacher_required 
def create_resource(request, *args, **kwargs):
    created = False
    
    # get data for base.html template
    context = {}
    context = base_data(context)

    # gets object being edited
    course = Course.objects.get(pk=kwargs.get('pk'))

    if request.method == 'POST':
        resource_form = ResourceForm(request.POST, request.FILES)
        resource_type_form = ResourceTypeForm(request.POST)

        # validate form data
        if resource_form.is_valid() and resource_type_form.is_valid():
            # save form  data
            resource = resource_form.save()
            resource.course = course
            resource.save()
            resource_type = resource_type_form.save(commit=False)
            resource_type.resource = resource
            resource_type.save()

            created = True
            return HttpResponseRedirect(reverse('course', args=[course.pk]))
    else:
        init_data = {'course': course}
        resource_form = ResourceForm(initial=init_data)
        resource_type_form = ResourceTypeForm()

    context['resource_form'] = resource_form
    context['resource_type_form'] = resource_type_form
    context['created'] = created
    # passes content for base template, and form
    return render(request, 'courses/add_resources.html', context)

def course_enrollment(request, *args, **kwargs):
    enrolled = False

    # get data for base.html template
    context = {}
    context = base_data(context)

    # gets object being used 
    course = Course.objects.get(pk=kwargs.get('pk'))
    student = Student.objects.get(user__pk=request.user.pk)

    enrollment_exist = student_course_enrollment(student, course)

    if request.method == 'POST' and enrollment_exist == False:
        # gets form
        enrollment_form = EnrollmentForm(request.POST)

        # validate form data
        if enrollment_form.is_valid():
            enrollment = enrollment_form.save(commit=False)
            enrollment.student = student
            enrollment.course = course
            enrollment.save()
            enrolled = True
            enrollment_exist = True
    else:
        init_data = {'student': student, 'course': course}
        enrollment_form = EnrollmentForm(initial=init_data)
    
    context['enrollment_form'] = enrollment_form
    context['course'] = course
    context['enrolled'] = enrolled
    context['enrollment_exist'] = enrollment_exist

    return render(request, 'courses/enrollment.html', context)


@login_required()
def course_unenrollment(request, *args, **kwargs):

    # get data for base.html template
    context = {}
    context = base_data(context)

    # finds enrollment
    enrollment = Enrollment.objects.get(pk=kwargs['pk'])

    if request.method == 'POST':
        # deletes enrollment
        enrollment.delete()
        if request.user.is_student:
            return HttpResponseRedirect('/student/enrollments')
        elif request.user.is_teacher:
            return HttpResponseRedirect('/teacher/students')
        
    context['enrollment'] = enrollment
    return render(request, 'courses/unenrollment.html', context)



# ============================helper functions ==================================

# verify enrollment exist
def student_course_enrollment(student, course):
    enrollment_exist = False
    try:
        student_courses = Enrollment.objects.filter(student__pk=student.pk).filter(course__pk=course.pk)
        if len(student_courses) > 0:
            enrollment_exist = True
    except:
        enrollment_exist = False

    return enrollment_exist
