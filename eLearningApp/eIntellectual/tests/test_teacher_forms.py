from datetime import date

from django.test import TestCase

from teachers.forms import TeacherForm

class TeacherFormTestCase(TestCase):
    def setUp(self):
        self.teacher_form = TeacherForm(data={
            'username': 'user1',
            'password1': 'longestpass098',
            'password2': 'longestpass098',
            'account_number': 'TCTC101080',
            'name': 'Teacher',
            'last_name': 'TcLastname',
            'birthday': date(1980,10,10),
            'email': 'teacher@email.com',
            'start_date': date(2022,10,15),
            'photo': 'image.png'
        })

    # Test Teacher form is valid
    def test_TeacherForm_valid(self):
        self.assertTrue(self.teacher_form.is_valid())

    # Test Course form is invalid
    def test_TeacherForm_invalid(self):
        teacher_form = TeacherForm(data={
            'account_number': ""
        })
        self.assertFalse(teacher_form.is_valid())
