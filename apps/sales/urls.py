# Django
from django.urls import path
# Apps
from . import views

app_name = "sales_app"

urlpatterns = [
    path('ventas/<str:local>/<int:month>/<int:year>', views.MonthSale.as_view(), name='resumen_sales'),
    path('ventas/<str:local>/<int:day>/<int:month>/<int:year>', views.DaySale.as_view(), name='day_sales'),
]
