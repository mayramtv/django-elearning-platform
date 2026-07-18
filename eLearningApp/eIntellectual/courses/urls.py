from django.urls import path
from . import views


urlpatterns = [
    path('courses/', views.CoursesList.as_view(), name='courses'),
    path('course/create/', views.create_course, name='create_course'),
    path('course/<int:pk>/delete/', views.CourseDelete.as_view(), name='delete'),
    path('course/<int:pk>/', views.CourseDetail.as_view(), name='course'),
    path('course/<int:pk>/add-resources/', views.create_resource, name='add_resources'),
    path('course/<int:pk>/enroll', views.course_enrollment, name='course_enrollment'),
    path('enrollment/<int:pk>/unenroll', views.course_unenrollment, name='course_unenrollment'),
]