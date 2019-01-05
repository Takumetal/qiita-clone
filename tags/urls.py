from django.urls import path

from . import views


app_name = 'tags'
urlpatterns = [
    path('tags/', views.TagListView.as_view(), name='list'),
    path('tags/<str:tag>/', views.TagDetailView.as_view(), name='detail'),
    path('tags/<str:tag>/follow/', views.TagFollowView.as_view(), name='follow'),
]
