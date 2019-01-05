from django.urls import path

from . import views


app_name = 'comments'
urlpatterns = [
    path('posts/<str:username>/<int:pk>/comment/', views.CommentView.as_view(), name='comment'),
    path('posts/<str:username>/<int:pk>/comment/good/', views.CommentGoodView.as_view(), name='good'),
]
