from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path('users/', views.UserListView.as_view(), name='list'),
    path('profile/<str:username>/', views.UserDetailView.as_view(), name='detail'),
    path('<str:username>/<int:pk>/edit/', views.UserEditView.as_view(), name='edit'),
    path('stock/', views.StockListView.as_view(), name='stock'),
    path('profile/<str:username>/follow/', views.UserFollowView.as_view(), name='follow'),
]
