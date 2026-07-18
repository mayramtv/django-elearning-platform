# Code References:
    # https://www.geeksforgeeks.org/how-to-spread-django-unit-tests-over-multiple-files/

from django.test import TestCase

from django.urls import reverse
from datetime import date

from management.models import User
from courses.models import Course
from teachers.models import Teacher

from courses.forms import CourseForm

class CreateCourseViewTestsCase(TestCase):
    def setUp(self):
        self.url = reverse('create_course')
        self.credentials = {'username':"Teacher1", 'password':'longestpass098'}
        self.user = User.objects.create(**self.credentials, is_teacher=True)
        self.teacher = Teacher.objects.create(user=self.user, name='Teacher')
        self.course_data = {'code': "CN0001", 
                            'teacher': self.teacher, 
                            'date_created': date(2022,10,15),
                            'date_updated': date(2022,10,16)}

    # Redirects to login when using GET request if user is NOT signed in 
    def test_create_course_view_get_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    # Renders template when using GET request if user signed in 
    def test_create_course_view_get(self):
        response = self.client.get("/teacher/login/?next=/course/create/", self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)

    # Renders template when using POST request if user signed in 
    def test_create_course_view_post(self):
        response = self.client.post("/teacher/login/?next=/course/create/", self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)

    # Redirects after creating course
    def test_create_course_after_login(self):
        # response = self.client.post('/teacher/login', self.credentials, follow=True)        
        response = self.client.post(self.url, self.course_data)
        self.assertEqual(response.status_code, 302)



    