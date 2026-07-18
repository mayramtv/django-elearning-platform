
from django.db.models.query import QuerySet
from django.db.models import Q
from django.views.generic import ListView, DeleteView, TemplateView

from django.shortcuts import render
from django.urls import reverse_lazy

from .models import User
from courses.models import Course, Enrollment
from students.models import Student
from teachers.models import Teacher

from .forms import SearchBoxForm

class DeleteAccount(DeleteView):
    model = User 
    success_url = "/"

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 

        # get data for base.html template
        context = base_data(context)
        return context

class SearchResultsView(ListView):
    model = User
    template_name = 'management/search_results.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 

        # return queryset
        query = self.request.GET.get('query')
        students_list = list(Student.objects.filter(Q(name__icontains=query) | Q(last_name__icontains=query)))
        teachers_list = list(Teacher.objects.filter(Q(name__icontains=query) | Q(last_name__icontains=query)))
        # combined_queryset = students_list + teachers_list
        context['students_list'] = students_list
        context['teachers_list'] = teachers_list

        # get data for base.html template
        context = base_data(context)
        return context


class IndexView(TemplateView):
    model = Course
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = None

        # passes the pk fro the home page
        if self.request.user.is_authenticated and self.request.user.is_student:
            user_pk = Student.objects.get(user__pk=self.request.user.pk).pk
        if self.request.user.is_authenticated and self.request.user.is_teacher:
            user_pk = Teacher.objects.get(user__pk=self.request.user.pk).pk
        context['user_pk'] = user_pk
        # get data for base.html template
        context = base_data(context)

        return context
    
    def get_template_names(self):
        return 'management/index.html' 
    
   

def management(request):
    return render(request, 'management/management.html', {'data': "Accounts Page"})

# ================================Function to share data between apps=====================================================
# returns data that needs to be used in each app view for the base.html
# ===========================Helper functions=========================================
    
def base_data(context):
    # request data for the base.html template
    base_data = base_template_data()

    # content for base template
    context['top_courses'] = base_data['top_courses']
    context['courses_by_category'] = base_data['courses_by_category']
    context['courses_count'] = base_data['courses_count']
    context['students_count'] =  base_data['students_count']

    return context

def base_template_data():
    try:
        courses_count = len(Course.objects.all())
    except Exception as e:
        courses_count = e
    try:
        students_count = len(Student.objects.all())
    except Exception as e:
        students_count = e
        
    base_data = {
        'top_courses': get_top_courses(),
        'courses_by_category': get_courses_by_category(),
        'courses_count': courses_count,
        'students_count': students_count
    }
    return base_data

# extract top courses
def get_top_courses():
    try:
        enrolled_courses = Enrollment.objects.values_list('course', flat=True)
        try:
            t_couses = {key:0 for key in set(enrolled_courses)}
            for c in enrolled_courses:
                t_couses[c] = t_couses[c] + 1
            sorted_top_couses = {key: value for key, value in sorted(t_couses.items(), key=lambda item: item[1], reverse=True)}.keys()
            top_courses = [Course.objects.get(id=pID) for i, pID in enumerate(sorted_top_couses) if i < 3]
        except:
            top_courses = []    
    except:
        top_courses = []

    return top_courses

# extract a dictionary of categories with a respective list of courses
def get_courses_by_category():
    try:
        categories = set(Course.objects.values_list('category', flat=True))
        try:
            courses_dict = {}
            for cat in categories:
                courses_dict[cat] = Course.objects.filter(category=cat)
        except:
            courses_dict = {}
    except:
        courses_dict = {}

    return courses_dict



