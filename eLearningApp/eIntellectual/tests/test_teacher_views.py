from django.test import TestCase

from management.models import User
from teachers.models import Teacher, TeacherStatus


class TeacherHomeViewTestsCase(TestCase):
    def setUp(self):
        User.objects.create(username='another-user')
        self.user = User.objects.create(username='teacher-user', is_teacher=True)
        self.teacher = Teacher.objects.create(user=self.user, name='Teacher')
        self.url = f'/teacher/home/{self.teacher.pk}'

    def test_teacher_navigation_uses_teacher_pk(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertContains(response, f'/teacher/home/{self.teacher.pk}')
        self.assertNotContains(response, f'/teacher/home/{self.user.pk}')

    def test_status_submission_redirects_to_teacher_home(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            {'content': 'Preparing a new course'},
        )

        self.assertRedirects(response, self.url)
        self.assertTrue(
            TeacherStatus.objects.filter(
                teacher=self.teacher,
                content='Preparing a new course',
            ).exists()
        )
