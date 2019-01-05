from django.urls import path

from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<str:username>/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('posts/create/', views.PostCreateView.as_view(), name='create'),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('posts/<str:username>/<int:pk>/good/', views.PostGoodView.as_view(), name='good'),
]
