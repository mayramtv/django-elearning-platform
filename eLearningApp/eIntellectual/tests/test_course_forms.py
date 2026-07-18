
from datetime import date

from django.test import TestCase

from teachers.models import Teacher
from students.models import Student
from courses.models import Course

from courses.forms import CourseForm, ResourceForm, EnrollmentForm

class CourseFormTestCase(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="Teacher", last_name="Lastname")
        self.course_form = CourseForm(data={
            'code': 'CS1001',
            'name': 'Computer Scince',
            'category': 'Computer Science',
            'teacher': self.teacher,
            'date_created': date(2022,10,15),
            'description': "Some text",
            'image': 'image.png'
        })

    # Test Course form is valid
    def test_CourseForm_valid(self):
        self.assertTrue(self.course_form.is_valid())

    # Test Course form is invalid
    def test_CourseForm_invalid(self):
        course_form = CourseForm(data={
            'code': ""
        })
        self.assertFalse(course_form.is_valid())

class ResourceFormTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(code='CS1001', name='Computer Scince')
        self.resource_form = ResourceForm(data={
            'code': 'CS1001.1',
            'course': self.course,
            'content': 'file.txt',
            'text': 'Some text' 
        })

    # Test Resource form is valid
    def test_ResourceForm_valid(self):
        self.assertTrue(self.resource_form.is_valid())

    # Test Resource form is invalid
    def test_ResourceForm_invalid(self):
        resource_form = ResourceForm(data={
            'code': ""
        })
        self.assertFalse(resource_form.is_valid())

class EnrollmentFormTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(user_name="user1")
        self.course = Course.objects.create(code='CS1001', name='Computer Scince')

    # Test Enrollment form is valid
    def test_EnrollmentForm_valid(self):
        enrollment_form = EnrollmentForm(data={
            'student': self.student,
            'course': self.course
        })
        self.assertTrue(enrollment_form.is_valid())
    
    # Test Enrollment form is invalid with no student
    def test_EnrollmentForm_invalid_no_student(self):
        enrollment_form = EnrollmentForm(data={
            'student': None,
            'course': self.course
        })
        self.assertFalse(enrollment_form.is_valid())

    # Test Enrollment form is invalid with no course
    def test_EnrollmentForm_invalid_no_course(self):
        enrollment_form = EnrollmentForm(data={
            'student': self.student,
            'course': None
        })
        self.assertFalse(enrollment_form.is_valid())

        