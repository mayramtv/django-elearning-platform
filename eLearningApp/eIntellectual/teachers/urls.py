from django.urls import path
from . import views

app_name = 'teacher'
urlpatterns = [
    path('home/<int:pk>', views.HomeDetails.as_view(), name='home'),
    path('profile/', views.ProfileDetails.as_view(), name='profile'),
    path('profile/update/<int:pk>', views.UpdateProfile.as_view(), name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),

    path('register/', views.register, name='register_teacher'),
    path('login/', views.login_teacher, name='login_teacher'),
    path('logout/', views.logout_teacher, name='logout_teacher'),
    
    path('classroom/', views.ClassroomList.as_view(), name='classroom'),
    path('students/', views.StudentsList.as_view(), name='students'),
]