from datetime import date

from django.test import TestCase

from students.forms import StudentForm

class StudentFormTestCase(TestCase):
    def setUp(self):
        self.student_form = StudentForm(data={
            'username': 'user1',
            'password1': 'longestpass098',
            'password2': 'longestpass098',
            'account_number': 'ACST101080',
            'name': 'Student',
            'last_name': 'StLastname',
            'birthday': date(1980,10,10),
            'email': 'student@email.com',
            'start_date': date(2022,10,15),
            'photo': 'image.png'
        })

    # Test Student form is valid
    def test_StudentForm_valid(self):
        self.assertTrue(self.student_form.is_valid())

    # Test Course form is invalid
    def test_StudentForm_invalid(self):
        student_form = StudentForm(data={
            'account_number': ""
        })
        self.assertFalse(student_form.is_valid())
