from django.shortcuts import render
from django.views.generic import (View, )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Sum
from django.db.models import Max, Min
from django.conf import settings

from apps.locals.models import Local
from apps.sales.models import Sales, ExcelSales
from apps.sales.forms import SalesForm

from openpyxl import Workbook
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
        l = Local.objects.get(slug=local)
        if not is_your_local(request.user, l):
            return redirect('users_app:user-login')

        today = datetime.datetime.today()
        if datetime.datetime(year, month, 1) > today:
            return redirect('sales_app:resumen_sales', local=l.slug, month=today.month, year=today.year)

        s = Sales.objects.filter(local=l)

        if s.exists():
            total_valor_venta = s.aggregate(Sum('sale_value'))
            t_c_u = s.aggregate(Sum('quantity_units'))
            t_c_t = s.aggregate(Sum('quantity_tickets'))
            total_valor_nc = s.aggregate(Sum('nc_value'))

            try:
                total_pxt = t_c_u['quantity_units__sum'] / t_c_t['quantity_tickets__sum']
            except ZeroDivisionError:
                total_pxt = 0

            try:
                total_precio_promedio = total_valor_venta['sale_value__sum'] / t_c_u['quantity_units__sum']
            except ZeroDivisionError:
                total_precio_promedio = 0

            try:
                total_ticket_promedio = total_valor_venta['sale_value__sum'] / t_c_t['quantity_tickets__sum']
            except ZeroDivisionError:
                total_ticket_promedio = 0

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
            'local': l,
            'month': month,
            'current_month': today.month,
            'today': today,
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

        num_days = calendar.monthrange(year, month)[1]
        days = [datetime.date(year, month, d) for d in range(1, num_days + 1)]

        return render(request, 'sales/day.html', {
            'locals': local_(self.request.user),
            'local': local,
            'day': day,
            'days': days,
            'month': month,
            'year': year,
            'month_name': months[month - 1],
            'exist': s.exists(),
            'sale': s,
            'sales_form': sales_form,
            'today': datetime.date.today(),
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


# SU
class PanelSu(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sales/admin/panel.html', {
            'locals': Local.objects.all(),
            'today': datetime.datetime.today()
        })


class MonthSaleSu(LoginRequiredMixin, View):
    def get(self, request, local, month, year, *args, **kwargs):
        today = datetime.datetime.today()
        days = []
        test_date = datetime.datetime(year, month, 1)
        days_month = list(range(1, int(calendar.monthrange(test_date.year, test_date.month)[1]) + 1))
        try:
            es = ExcelSales.objects.get(local__slug=local, date__month=month, date__year=year)
            excel = {
                'is_excel': True,
                'es': es
            }
        except:
            excel = {
                'is_excel': False,
                'es': ''
            }

        for d in days_month:
            try:
                s = Sales.objects.get(local__slug=local, date__day=d, date__month=month, date__year=year)
                days.append({
                    'day': d,
                    'sale_value': s.sale_value,
                    'quantity_tickets': s.quantity_tickets,
                    'can_edit': s.can_edit,
                })
            except:
                days.append({
                    'day': d,
                    'sale_value': 0,
                    'quantity_tickets': 0,
                    'can_edit': True,
                })

        d_max = Sales.objects.aggregate(Max('date'))
        d_min = Sales.objects.aggregate(Min('date'))

        return render(request, 'sales/admin/list.html', {
            'local': Local.objects.get(slug=local),
            'locals': Local.objects.all(),
            'today': today,
            'days': days,
            'month': month,
            'months': months,
            'month_name': months[month - 1],
            'year': year,
            'excel': excel,
            'years': list(range(d_min['date__min'].year, int(d_max['date__max'].year) + 2)),
        })


class LockMonthSu(LoginRequiredMixin, View):
    def post(self, request, local, month, year, *args, **kwargs):
        num_days = calendar.monthrange(year, month)[1]
        days = [datetime.date(year, month, day) for day in range(1, num_days + 1)]

        for d in days:
            try:
                s = Sales.objects.get(
                    local__slug=local,
                    date__day=d.day,
                    date__month=month,
                    date__year=year
                )
                s.can_edit = False
                s.save()
            except:
                s = Sales.objects.create(
                    local=Local.objects.get(slug=local),
                    date=datetime.datetime(year, month, d.day),
                    sale_value=float(0),
                    quantity_units=float(0),
                    quantity_tickets=float(0),
                    nc_value=float(0),
                    can_edit=False
                )
        return redirect('sales_app:r_sales_su', local=local, month=month, year=year)


class UnlockMonthSu(LoginRequiredMixin, View):
    def post(self, request, local, month, year, *args, **kwargs):
        Sales.objects.filter(
            local__slug=local,
            date__month=month,
            date__year=year
        ).update(can_edit=True)

        return redirect('sales_app:r_sales_su', local=local, month=month, year=year)


class GenerateExcel(LoginRequiredMixin, View):
    def post(self, request, local, month, year, *args, **kwargs):
        num_days = calendar.monthrange(year, month)[1]
        days = [datetime.date(year, month, day) for day in range(1, num_days + 1)]

        wb = Workbook()
        ws = wb.active
        ws.append([
            'Fecha',
            'Cantidad',
            'Importe',
        ])

        for d in days:
            sl = []
            try:
                s = Sales.objects.get(
                    local__slug=local,
                    date__day=d.day,
                    date__month=month,
                    date__year=year
                )
                sl.append(s.date)
                sl.append(s.sale_value)
                sl.append(s.quantity_tickets)
            except:
                sl.append('{}/{}/{}'.format(year, month, d.day))
                sl.append('0')
                sl.append('0')
            ws.append(sl)

        url = '{}/media/xls/{}-{}-{}.xlsx'.format(settings.BASE_DIR, local, month, year)

        wb.save(url)
        ExcelSales.objects.create(
            local=Local.objects.get(slug=local),
            date=datetime.datetime(year, month, 1),
            url='/media/xls/{}-{}-{}.xlsx'.format(local, month, year),
        )
        return redirect('sales_app:r_sales_su', local=local, month=month, year=year)


class ChangeDate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        return redirect(
            'sales_app:r_sales_su',
            local=request.GET.get('local'),
            month=request.GET.get('month'),
            year=request.GET.get('year')
        )
