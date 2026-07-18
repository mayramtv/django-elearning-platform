
from django.test import TestCase

from students.models import Student
from management.models import User

class StudentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.student = Student.objects.create(user=self.user)
    
    def test_student_user_relationship(self):
        student = Student.objects.get(user__username='user1')
        self.assertTrue(isinstance(student, Student))