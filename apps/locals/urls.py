# Django
from django.urls import path
# Apps
from . import views

app_name = "locals_app"

urlpatterns = [
    path('panel', views.PanelView.as_view(), name='panel'),
    path('<str:local>/gerente/agregar', views.ManagerCreateView.as_view(), name='manager-add'),
    path('<str:local>/gerente/<pk>/', views.ManagerUpdateView.as_view(), name='manager-update'),
    path('gerente/eliminar/<pk>/', views.ManagerDeleteView.as_view(), name='manager-delete'),

    path('<str:local>/empleado/agregar', views.EmployeeCreateView.as_view(), name='employee-add'),
    path('<str:local>/empleado/<pk>/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('empleado/eliminar/<pk>/', views.EmployeeDeleteView.as_view(), name='employee-delete'),
]
