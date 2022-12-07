from django.shortcuts import render
from django.views.generic import (View, )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Sum
from django.db.models import Max, Min

from apps.locals.models import Local
from apps.sales.models import Sales
from apps.sales.forms import SalesForm

import datetime
import calendar
months = (
    "Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre",
    "Diciembre"
)


# Function
def local_(user):
    if user.type_user == '1':
        return Local.objects.filter(owner=user)
    elif user.type_user == '2':
        return Local.objects.filter(manager__manager=user)


# views
def is_your_local(user, local):
    if user.type_user == '1':
        exist = Local.objects.filter(name=local, owner=user).exists()
    elif user.type_user == '2':
        exist = Local.objects.filter(name=local, manager__manager=user).exists()
    return exist


class MonthSale(LoginRequiredMixin, View):
    def get(self, request, local, month, year, *args, **kwargs):
        local = Local.objects.get(slug=local)
        if not is_your_local(request.user, local):
            return redirect('users_app:user-login')

        today = datetime.datetime.today()
        if datetime.datetime(year, month, 1) > today:
            return redirect('sales_app:resumen_sales', local=local.slug, month=today.month, year=today.year)

        s = Sales.objects.filter(local=local, date__month=month, date__year=year)

        if s.exists():
            total_valor_venta = s.aggregate(Sum('sale_value'))
            t_c_u = s.aggregate(Sum('quantity_units'))
            t_c_t = s.aggregate(Sum('quantity_tickets'))
            total_valor_nc = s.aggregate(Sum('nc_value'))

            total_pxt = t_c_u['quantity_units__sum'] / t_c_t['quantity_tickets__sum']
            total_precio_promedio = total_valor_venta['sale_value__sum'] / t_c_u['quantity_units__sum']
            total_ticket_promedio = total_valor_venta['sale_value__sum'] / t_c_t['quantity_tickets__sum']

            d_max = Sales.objects.aggregate(Max('date'))
            d_min = Sales.objects.aggregate(Min('date'))
        else:
            total_valor_venta = {'sale_value__sum': 0}
            t_c_u = {'quantity_units__sum': 0}
            t_c_t = {'quantity_tickets__sum': 0}
            total_valor_nc = {'nc_value__sum': 0}

            total_pxt = 0
            total_precio_promedio = 0
            total_ticket_promedio = 0

            d_max = {'date__max': today}
            d_min = {'date__min': today}

        return render(request, 'sales/list.html', {
            'locals': local_(self.request.user),
            'local': local,
            'month': month,
            'current_month': today.month,
            'months': [
                'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                'Noviembre', 'Diciembre'
            ],
            'year': year,
            'years': list(range(d_min['date__min'].year, int(d_max['date__max'].year) + 2)),
            'month_name': months[month - 1],

            'total_valor_venta': total_valor_venta['sale_value__sum'],
            'total_cantidad_unidades': t_c_u['quantity_units__sum'],
            'total_cantidad_tickets': t_c_t['quantity_tickets__sum'],
            'total_valor_nc': total_valor_nc['nc_value__sum'],

            'total_pxt': total_pxt,
            'total_precio_promedio': total_precio_promedio,
            'total_ticket_promedio': total_ticket_promedio,
        })


class DaySale(LoginRequiredMixin, View):
    def get(self, request, local, day, month, year, *args, **kwargs):
        local = Local.objects.get(slug=local)
        if not is_your_local(request.user, local):
            return redirect('users_app:user-login')

        today = datetime.datetime.today()
        if datetime.datetime(year, month, day) > today:
            return redirect('sales_app:day_sales', local=local.slug, day=today.day, month=today.month, year=today.year)

        ss = Sales.objects.filter(local=local, date__month=month, date__year=year)
        s = ss.filter(date__day=day)

        if s.exists():
            sales_form = SalesForm(instance=s[0])
        else:
            sales_form = SalesForm()

        test_date = datetime.datetime(year, month, day)

        return render(request, 'sales/day.html', {
            'locals': local_(self.request.user),
            'local': local,
            'days': list(range(1, int(calendar.monthrange(test_date.year, test_date.month)[1]) + 1)),
            'day': day,
            'month': month,
            'year': year,
            'month_name': months[month - 1],
            'exist': s.exists(),
            'sale': s,
            'sales_form': sales_form,
            'today': today,
        })

    def post(self, request, local, day, month, year, *args, **kwargs):
        s = Sales.objects.filter(local__slug=local, date__day=day, date__month=month, date__year=year)
        if s.exists():
            s.update(
                sale_value=float(request.POST.get('sale_value')),
                quantity_units=float(request.POST.get('quantity_units')),
                quantity_tickets=float(request.POST.get('quantity_tickets')),
                nc_value=float(request.POST.get('nc_value')),
                observations=request.POST.get('observations')
            )
        else:
            s = SalesForm(request.POST)
            if s.is_valid():
                Sales.objects.create(
                    local=Local.objects.get(slug=local),
                    date=datetime.datetime(year, month, day),
                    sale_value=float(s.cleaned_data.get('sale_value')),
                    quantity_units=float(s.cleaned_data.get('quantity_units')),
                    quantity_tickets=float(s.cleaned_data.get('quantity_tickets')),
                    nc_value=float(s.cleaned_data.get('nc_value')),
                    observations=s.cleaned_data.get('observations')
                )

        return redirect('sales_app:day_sales', local=local, day=day, month=month, year=year)
