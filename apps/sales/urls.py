# Django
from django.urls import path
# Apps
from . import views

app_name = "sales_app"

urlpatterns = [
    path('', views.SalesView.as_view(), name='sales'),
]
