
# I write the following code following the following guidlines, documentation and classes
    # University of London Advance Web Development module
    # Lectures and Labs presented by Dr Daniel Buchan
    # https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html

from django.utils.decorators import method_decorator

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.views.generic import ListView, TemplateView, UpdateView, DetailView

from management.views import base_template_data, base_data

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .forms import TeacherForm, TeacherProfileForm, TeacherStatusForm

from .models import Teacher, TeacherStatus
from courses.models import Course, Enrollment
from students.models import Student

from management.decorators import teacher_required

# Public profile
class HomeDetails(DetailView):
    model = Teacher
    template_name = 'teachers/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own_status = False

        # gets current teacher's courses and profile
        teacher = Teacher.objects.get(pk=kwargs['object'].pk)
        classroom_courses = Course.objects.filter(teacher__pk=teacher.pk).order_by('-date_created')
        context['number_courses'] = len(classroom_courses)
        context['classroom_courses'] = classroom_courses[0:3]
        context['teacher'] = teacher
        context['status_form'] = TeacherStatusForm(initial={'teacher':teacher})
        context['status_list'] = TeacherStatus.objects.filter(teacher__pk=teacher.pk).order_by('-timestamp')[:3]

        if self.request.user.is_authenticated and self.request.user.is_teacher:
            if self.request.user.pk == teacher.user.pk:
                own_status = True
        context['own_status'] = own_status
        
        # get data for base.html template
        context = base_data(context)
        return context
    
    def post(self, request, *args, **kwargs):
        # get form and passes the comment information
        status_form = TeacherStatusForm(data=self.request.POST)
        if status_form.is_valid():
            status = status_form.save(commit=False)
            status.teacher = Teacher.objects.get(user__pk=self.request.user.pk)                # grabs teacher from  passes it to status.teacher
            status.save()                                 
            return HttpResponseRedirect(f'/teacher/home/{status.teacher.pk}')
        return self.get(request, *args, **kwargs)

        
        


# Private profile
@method_decorator([login_required(login_url='/teacher/login'), teacher_required(login_url='/teacher/login')], name='dispatch')
class ProfileDetails(TemplateView):
    model = Teacher
    template_name = 'teachers/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # gets current teacher's courses and profile
        teacher = Teacher.objects.get(user__pk=self.request.user.pk)
        context['teacher'] = teacher

        # get data for base.html template
        context = base_data(context)
        return context
    
@method_decorator([login_required(login_url='/teacher/login'), teacher_required(login_url='/teacher/login')], name='dispatch') 
class UpdateProfile(UpdateView):
    model = Teacher
    fields = ['name', 'last_name', 'email', 'photo']
    template_name = 'teachers/profile_update_form.html'
    success_url = '/teacher/profile'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 

        # get data for base.html template
        context = base_data(context)
        return context

# The provenance of the following function code is from the bioweb app from the refernce mentioned above
@login_required(login_url='/teacher/login')
@teacher_required(login_url='/teacher/login')
def change_password(request):
    # get data for base.html template
    context = {}
    context = base_data(context)

    updated  = False
    if request.method == 'POST':
        # get password change form and passes the user information
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            updated = True
            update_session_auth_hash(request, form.user)
    else:
        form = PasswordChangeForm(request.user)
    
    context['form'] = form
    context['updated'] = updated
    return render(request, 'teachers/change_password.html', context)


# logout users
def logout_teacher(request):
    logout(request)
    return HttpResponseRedirect('/')


# The provenance of the following function code is from the bioweb app from the refernce mentioned above
def login_teacher(request):
    # get data for base.html template
    context = {}
    context = base_data(context)

    if request.method == 'POST':
        # gets values from request
        username = request.POST['username']
        password = request.POST['password']

        # authenticate user
        user = authenticate(request,
                            username=username, 
                            password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/teacher/profile')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid username or password.")
    else:
        context['user_type'] = 'teacher'
        return render(request, 'teachers/login.html', context)


# The structure of the following function code is from the refernce mentioned above
def register(request):
    registered = False

    # get data for base.html template
    context = {}
    context = base_data(context)

    if request.method == 'POST':
        teacher_form = TeacherForm(data=request.POST)
        teacher_profile_form = TeacherProfileForm(request.POST, request.FILES)

        # validate form data
        if teacher_form.is_valid() and teacher_profile_form.is_valid():
            # save user and profile form  data
            user = teacher_form.save(commit=False)
            user.is_teacher = True                              # sets user as teacher
            user.save()
            profile = teacher_profile_form.save(commit=False)
            profile.user_name = user.username                   # grabs username from user and passes it to teacher profile
            profile.user = user                                 # connects user to teacher user profile
            profile.save()

            registered = True

    else:
        teacher_form = TeacherForm()
        teacher_profile_form = TeacherProfileForm()

    context['teacher_form'] = teacher_form
    context['teacher_profile_form'] = teacher_profile_form
    context['registered'] = registered
    context['user_type'] = 'teacher'
    return render(request, 'teachers/register.html', context)

@method_decorator([login_required(login_url='/teacher/login'), teacher_required(login_url='/teacher/login')], name='dispatch')
class ClassroomList(ListView):
    model = Course
    context_object_name = 'classroom_list'
    template_name = 'teachers/classroom.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # gets current teacher's courses
        teacher = Teacher.objects.get(user__pk=self.request.user.pk)
        classroom_courses = Course.objects.filter(teacher__pk=teacher.pk)
        context['classroom_courses'] = classroom_courses
        context['teacher'] = teacher
        context = base_data(context)
        return context

@method_decorator([login_required(login_url='/teacher/login'), teacher_required(login_url='/teacher/login')], name='dispatch')
class StudentsList(ListView):
    model = Student
    template_name = 'teachers/students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # gets current teacher's courses
        teacher = Teacher.objects.get(user__pk=self.request.user.pk)
        classroom_courses = Course.objects.filter(teacher__pk=teacher.pk)

        enrollments_list = {}
        for course in classroom_courses:
            enrollments_list[course.code] = [enroll for enroll in Enrollment.objects.filter(course__pk=course.pk)]

        context['enrollments_list'] = enrollments_list
        context['teacher'] = teacher
        context = base_data(context)
        return context
