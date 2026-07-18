from django.urls import path
from . import views

urlpatterns = [
    path('home/<int:pk>', views.HomeDetails.as_view(), name='home'),
    path('profile/', views.ProfileDetails.as_view(), name='profile'),
    path('profile/update/<int:pk>', views.UpdateProfile.as_view(), name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),

    path('register/', views.register, name='register_student'),
    path('login/', views.login_student, name='login_student'),
    path('logout/', views.logout_student, name='logout_student'),

    path('enrollments/', views.EnrollmentsList.as_view(), name='enrrolments_list'),
]