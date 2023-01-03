# Django
from django.urls import path
# Apps
from . import views

app_name = "sales_app"

urlpatterns = [
    path('ventas/<str:local>/<int:month>/<int:year>', views.MonthSale.as_view(), name='resumen_sales'),
    path('ventas/<str:local>/<int:day>/<int:month>/<int:year>', views.DaySale.as_view(), name='day_sales'),

    path('administrador/ventas/', views.PanelSu.as_view(), name='panel_su'),
    path('administrador/ventas/<str:local>/<int:month>/<int:year>', views.MonthSaleSu.as_view(), name='r_sales_su'),
]
