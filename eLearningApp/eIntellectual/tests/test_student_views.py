

from django.test import TestCase

from django.urls import reverse
from datetime import date

from management.models import User
from students.models import Student, StudentStatus

class StudentHomeViewTestsCase(TestCase):
    def setUp(self):
        self.credentials = {'username':"Student", 'password':'longestpass098'}
        self.user = User.objects.create(**self.credentials, is_student=True)
        self.teacher = Student.objects.create(user=self.user, name='Student')
        self.url = '/student/home/' 

    # Returns status code 200 when using GET request if user signed in 
    def test_student_home_view_get_200(self):
        url_good_pk = self.url + str(self.user.pk)
        response = self.client.get(url_good_pk)
        self.assertEqual(response.status_code, 200)

    # Returns status code 200 when using GET request if user signed in but pk is not correct
    def test_student_home_view_get_404(self):
        url_bad_pk = self.url + str(100)
        response = self.client.get(url_bad_pk)
        self.assertEqual(response.status_code, 404)

    def test_student_navigation_uses_student_pk(self):
        User.objects.create(username='another-user')
        student_user = User.objects.create(username='student-user', is_student=True)
        student = Student.objects.create(user=student_user, name='Student')
        self.client.force_login(student_user)

        response = self.client.get(self.url + str(student.pk))

        self.assertContains(response, f'/student/home/{student.pk}')
        self.assertNotContains(response, f'/student/home/{student_user.pk}')

    def test_status_submission_redirects_to_student_home(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url + str(self.teacher.pk),
            {'content': 'Working on my course'},
        )

        self.assertRedirects(response, self.url + str(self.teacher.pk))
        self.assertTrue(
            StudentStatus.objects.filter(
                student=self.teacher,
                content='Working on my course',
            ).exists()
        )

class StudentProfileViewTestCase(TestCase):
    def setUp(self):
        self.credentials = {'username':"Student", 'password':'longestpass098'}
        self.user = User.objects.create(**self.credentials, is_student=True)
        self.teacher = Student.objects.create(user=self.user, name='Student')
        self.url = '/student/profile/'

    # Redirects to login when using GET request if user is NOT signed in 
    def test_student_profile__view_get_redirect(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    # Returns status code 200 when using GET request if user signed in 
    def test_student_profile_view_get(self):
        # response = self.client.get("/student/login/?next=" + self.url, self.credentials, follow=True)
        response = self.client.post(self.url, self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)

        
