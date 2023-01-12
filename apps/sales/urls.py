# Django
from django.urls import path
# Apps
from . import views

app_name = "sales_app"

urlpatterns = [
    path('ventas/<str:local>/<int:month>/<int:year>', views.MonthSale.as_view(), name='resumen_sales'),
    path('ventas/<str:local>/<int:day>/<int:month>/<int:year>', views.DaySale.as_view(), name='day_sales'),

    path('administrador/ventas/', views.PanelSu.as_view(), name='panel_su'),
    path(
        'administrador/ventas/<str:local>/<int:month>/<int:year>',
        views.MonthSaleSu.as_view(),
        name='r_sales_su'
    ),
    path(
        'administrador/bloquear_mes/<str:local>/<int:month>/<int:year>',
        views.LockMonthSu.as_view(),
        name='lock_month_su'
    ),
    path(
        'administrador/desbloquear_mes/<str:local>/<int:month>/<int:year>',
        views.UnlockMonthSu.as_view(),
        name='unlock_month_su'
    ),
    path(
        'administrador/desbloquear_mes/<str:local>/<int:month>/<int:year>',
        views.GenerateExcel.as_view(),
        name='unlock_month_su'
    ),
    path(
        'administrador/generar-excel/<str:local>/<int:month>/<int:year>',
        views.GenerateExcel.as_view(),
        name='generate_excel'
    ),
    path(
        'administrador/change-date',
        views.ChangeDate.as_view(),
        name='change_date'
    ),
]
