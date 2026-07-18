
# Code Reference
# The provenance of the following two functions is the following: 
    # https://github.com/sibtc/django-multiple-user-types-example/blob/master/django_school/classroom/decorators.py

from django.contrib.auth.decorators import user_passes_test

def student_required(function=None, redirect_field_name='next', login_url=None):

    def check_login(user):
        if user.is_authenticated and user.is_student:
            return True
        return False
    
    actual_decorator = user_passes_test(
        check_login,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator

def teacher_required(function=None, redirect_field_name='next', login_url=None):

    def check_login(user):
        if user.is_authenticated and user.is_teacher:
            return True
        return False
    
    actual_decorator = user_passes_test(
        check_login,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
    
    
