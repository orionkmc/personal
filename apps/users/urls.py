# Django
from django.urls import path
# Apps
from . import views

app_name = "users_app"

urlpatterns = [
    path('login', views.LoginUser.as_view(), name='user-login'),
    path('logout', views.LogoutView.as_view(), name='user-logout'),
]
