from django.db import models

from django.contrib.auth.models import AbstractUser


# The following class is from https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
class User(AbstractUser):

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


