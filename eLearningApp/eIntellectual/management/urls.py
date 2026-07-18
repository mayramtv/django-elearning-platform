from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search', views.SearchResultsView.as_view(), name='search_results'),
    path('management/', views.management, name='management'), # not in use
    path('delete-account/<int:pk>', views.DeleteAccount.as_view(), name='delete_account'),
]
