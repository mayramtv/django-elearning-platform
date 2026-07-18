
from django.test import TestCase

from teachers.models import Teacher
from management.models import User

class TeacherTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='teacher2')
        self.student = Teacher.objects.create(user=self.user)
    
    def test_student_user_relationship(self):
        student = Teacher.objects.get(user__username='teacher2')
        self.assertTrue(isinstance(student, Teacher))