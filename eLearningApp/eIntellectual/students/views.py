
# I write the following code following the following guidelines, documentation and classes
    # University of London Advance Web Development module
    # Lectures and Labs presented by Dr Daniel Buchan
    # https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
from django.utils.decorators import method_decorator

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse


from django.views.generic import ListView, DetailView, TemplateView, UpdateView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .forms import *

from .models import Student, StudentStatus
from courses.models import Enrollment

from management.views import base_data

from management.decorators import student_required

class HomeDetails(DetailView):
    model = Student
    template_name = 'students/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        own_status = False

        # gets current student's courses and home page information 
        student = Student.objects.get(pk=kwargs['object'].pk)
        enrollments_list = Enrollment.objects.filter(student__pk=student.pk).order_by('-date')
        context['number_courses'] = enrollments_list.count()
        context['enrollments_list'] = [e.course for e in enrollments_list][:3]
        context['student'] = student
        context['status_form'] = StudentStatusForm(initial={'student':student})
        context['status_list'] = StudentStatus.objects.filter(student__pk=student.pk).order_by('-timestamp')[:3]

        if self.request.user.is_authenticated:
            if self.request.user.is_student:
                if self.request.user.pk == student.user.pk:
                    own_status = True
            context['own_status'] = own_status
        
        # get data for base.html template
        context = base_data(context)
        return context
    
    def post(self, request, *args, **kwargs):
        # get form and passes the comment information
        status_form = StudentStatusForm(data=self.request.POST)
        if status_form.is_valid():
            status = status_form.save(commit=False)
            status.student = Student.objects.get(user__pk=self.request.user.pk)                # grabs student from  passes it to status.student
            status.save()                                 
            return HttpResponseRedirect(f'/student/home/{status.student.pk}')
        return self.get(request, *args, **kwargs)
    
# Private profile
@method_decorator([login_required(login_url='/student/login'), student_required(login_url='/student/login')], name='dispatch')
class ProfileDetails(TemplateView):
    model = Student
    template_name = 'students/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # gets current student's courses and private profile of user
        student = Student.objects.get(user__pk=self.request.user.pk)
        context['student'] = student

        # get data for base.html template
        context = base_data(context)
        return context
    
@method_decorator([login_required(login_url='/student/login'), student_required(login_url='/student/login')], name='dispatch')
class UpdateProfile(UpdateView):
    model = Student
    fields = ['name', 'last_name', 'email', 'photo']
    template_name = 'students/profile_update_form.html'
    success_url = '/student/profile'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 

        # get data for base.html template
        context = base_data(context)
        return context
    
# The provenance of the following function code is from the bioweb app from the refernce mentioned above
@login_required(login_url='/student/login')
@student_required(login_url='/student/login')
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
    return render(request, 'students/change_password.html', context)
        

# logout users
@login_required(login_url='/student/login')
def logout_student(request):
    logout(request)
    return HttpResponseRedirect('/')


# The provenance of the following function code is from the bioweb app from the refernce mentioned above
def login_student(request):
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
                return HttpResponseRedirect('/student/profile')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid username or password.")
    else:
        context['user_type'] = 'student'
        return render(request, 'students/login.html', context)

        
# The structure of the following function code is from the refernce mentioned above
def register(request):
    registered = False

    # get data for base.html template
    context = {}
    context = base_data(context)

    if request.method == 'POST':
        student_form = StudentForm(data=request.POST)
        student_profile_form = StudentProfileForm(request.POST, request.FILES)

        # validate form data
        if student_form.is_valid() and student_profile_form.is_valid():
            # save user and profile form  data
            user = student_form.save(commit=False)
            user.is_student = True                              # sets user as student
            user.save()
            profile = student_profile_form.save(commit=False)
            profile.user_name = user.username                   # grabs username from user and passes it to student profile
            profile.user = user                                 # connects user to student user profile
            profile.save()

            registered = True
    else:
        student_form = StudentForm()
        student_profile_form = StudentProfileForm()

    context['student_form'] = student_form
    context['student_profile_form'] = student_profile_form
    context['registered'] = registered
    context['user_type'] = 'student'
    return render(request, 'students/register.html', context)


@method_decorator([login_required(login_url='/student/login'), student_required(login_url='/student/login')], name='dispatch')
class EnrollmentsList(ListView):
    model = Enrollment
    context_object_name = 'enrollments_list'
    template_name = 'students/enrollments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        # gets current student 
        student = Student.objects.get(user__pk=self.request.user.pk)
        enrollments_list =  Enrollment.objects.filter(student__pk=student.pk)
        context['enrollments_list'] = enrollments_list
        # context['enrollments_list'] = [e.course for e in enrollments_list]
        context = base_data(context)
        return context
