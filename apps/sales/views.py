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
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre",
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

        s = Sales.objects.filter(local=l, date__month=month, date__year=year)
        a = s.filter(date__month=month, date__year=year, can_edit=False)
        num_days = calendar.monthrange(year, month)[1]
        if num_days == len(a):
            month_locked = True
        else:
            month_locked = False
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

            try:
                d_max = Sales.objects.get(local__slug=local).aggregate(Max('date'))
            except:
                d_max = {'date__max': today}

            try:
                d_min = Sales.objects.get(local__slug=local).aggregate(Min('date'))
            except:
                d_min = {'date__min': today}

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
                'Enero', 'Febrero', 'Marzo', 'Abrlil', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
                'Noviembre', 'Diciembre'
            ],
            'year': year,
            'years': list(range(d_min['date__min'].year - 1, int(d_max['date__max'].year) + 2)),
            'month_name': months[month - 1],
            'month_locked': month_locked,
            'total_valor_venta': round(total_valor_venta['sale_value__sum'], 2),
            'total_cantidad_tickets': round(t_c_t['quantity_tickets__sum']),
            'total_cantidad_unidades': round(t_c_u['quantity_units__sum']),
            'total_valor_nc': round(total_valor_nc['nc_value__sum']),

            'total_pxt': round(total_pxt),
            'total_precio_promedio': round(total_precio_promedio, 2),
            'total_ticket_promedio': round(total_ticket_promedio, 2),
        })


class DaySale(LoginRequiredMixin, View):
    def get(self, request, local, day, month, year, *args, **kwargs):
        local = Local.objects.get(slug=local)
        if not is_your_local(request.user, local):
            return redirect('users_app:user-login')

        today = datetime.datetime.today()
        if datetime.datetime(year, month, day) > today:
            return redirect('sales_app:day_sales', local=local.slug, day=today.day, month=today.month, year=today.year)

        s = Sales.objects.filter(local=local, date__day=day, date__month=month, date__year=year)

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
                    'nc_value': s.nc_value,
                    'observations': s.observations,
                    'can_edit': s.can_edit,
                })
            except:
                days.append({
                    'day': d,
                    'sale_value': 0,
                    'quantity_tickets': 0,
                    'nc_value': 0,
                    'observations': '',
                    'can_edit': True,
                })
        try:
            d_max = Sales.objects.get(local__slug=local).aggregate(Max('date'))
        except:
            d_max = {'date__max': today}

        try:
            d_min = Sales.objects.get(local__slug=local).aggregate(Min('date'))
        except:
            d_min = {'date__min': today}

        a = Sales.objects.filter(local__slug=local, date__month=month, date__year=year, can_edit=False)
        num_days = calendar.monthrange(year, month)[1]
        if num_days == len(a):
            month_locked = True
        else:
            month_locked = False

        s = Sales.objects.filter(local__slug=local, date__month=month, date__year=year)

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

            try:
                d_max = Sales.objects.get(local__slug=local).aggregate(Max('date'))
            except:
                d_max = {'date__max': today}

            try:
                d_min = Sales.objects.get(local__slug=local).aggregate(Min('date'))
            except:
                d_min = {'date__min': today}
            
            try:
                total_nc = round(total_valor_venta['sale_value__sum'], 2) - round(total_valor_nc['nc_value__sum'])
            except:
                total_nc = 0

        else:
            total_valor_venta = {'sale_value__sum': 0}
            t_c_u = {'quantity_units__sum': 0}
            t_c_t = {'quantity_tickets__sum': 0}
            total_valor_nc = {'nc_value__sum': 0}
            total_nc = { 'total_nc': 0 }

            total_pxt = 0
            total_precio_promedio = 0
            total_ticket_promedio = 0

            d_max = {'date__max': today}
            d_min = {'date__min': today}

        return render(request, 'sales/admin/list.html', {
            'local': Local.objects.get(slug=local),
            'locals': Local.objects.all(),
            'today': today,
            'days': days,
            'month': month,
            'months': months,
            'month_name': months[month - 1],
            'month_locked': month_locked,
            'year': year,
            'excel': excel,
            'years': list(range(d_min['date__min'].year - 1, int(d_max['date__max'].year) + 2)),

            'total_valor_venta': round(total_valor_venta['sale_value__sum'], 2),
            'total_cantidad_unidades': round(t_c_u['quantity_units__sum']),
            'total_cantidad_tickets': round(t_c_t['quantity_tickets__sum']),
            'total_valor_nc': round(total_valor_nc['nc_value__sum']),
            'total_nc': total_nc,

            'total_pxt': round(total_pxt),
            'total_precio_promedio': round(total_precio_promedio, 2),
            'total_ticket_promedio': round(total_ticket_promedio, 2),
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
        es = ExcelSales.objects.filter(local__slug=local, date__month=month, date__year=year)
        if es.exists():
            es.delete()

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
            'Total con NC',
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
                sl.append(s.total_nc)
                sl.append(s.quantity_tickets)
            except:
                sl.append('{}/{}/{}'.format(year, month, d.day))
                sl.append('0')
                sl.append('0')
                sl.append('0')
            ws.append(sl)

        base_url = '/media/xls/{}-{}.xlsx'.format(local, datetime.datetime.now())
        url = '{}{}'.format(settings.BASE_DIR, base_url)

        wb.save(url)
        ExcelSales.objects.create(
            local=Local.objects.get(slug=local),
            date=datetime.datetime(year, month, 1),
            url=base_url,
        )
        return redirect('sales_app:r_sales_su', local=local, month=month, year=year)


class ChangeDate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # from apps.users.models import User

        # a = [
        #     {'id': '101', 'name': 'METERETES', 'pass': '2bf577f6'},
        #     {'id': '102', 'name': 'STARBUCKS COFFEE ARGENTINA', 'pass': '537b2639'},
        #     {'id': '103', 'name': 'PROTOTYPE', 'pass': '05cc7c94'},
        #     {'id': '105', 'name': 'PENSEL', 'pass': 'f3919921'},
        #     {'id': '106', 'name': 'BUDDIES', 'pass': '524350cb'},
        #     {'id': '107', 'name': 'VIAMO', 'pass': '93bbd754'},
        #     {'id': '108', 'name': 'MIMO & CO', 'pass': 'a65121a6'},
        #     {'id': '110', 'name': 'ADVANCED', 'pass': '1e8ce8c9'},
        #     {'id': '111', 'name': 'TED BODIN', 'pass': 'e6d94e49'},
        #     {'id': '112', 'name': 'CARDON', 'pass': '988a4585'},
        #     {'id': '113', 'name': 'WANAMA', 'pass': 'bc246b52'},
        #     {'id': '114', 'name': 'TUCCI', 'pass': '43bbe9b6'},
        #     {'id': '115', 'name': 'SPORTLINE', 'pass': '0f656039'},
        #     {'id': '117', 'name': 'TORQUE', 'pass': 'dd4d7e7a'},
        #     {'id': '118', 'name': 'OLD BRIDGE', 'pass': '616c1239'},
        #     {'id': '119', 'name': 'SWEET', 'pass': 'd2e58a42'},
        #     {'id': '120', 'name': '47 STREET', 'pass': 'fe843b9e'},
        #     {'id': '121', 'name': 'LEVIS', 'pass': '1e10fcfb'},
        #     {'id': '122', 'name': 'COMO QUIERES QUE TE QUIERA', 'pass': '7f9ddba0'},
        #     {'id': '123', 'name': 'VACIO', 'pass': 'b39a0c3e'},
        #     {'id': '124', 'name': 'XL EXTRA LARGE', 'pass': 'fdce675b'},
        #     {'id': '125', 'name': 'CHEEKY', 'pass': 'ece570fc'},
        #     {'id': '129', 'name': 'GRISINO', 'pass': 'b5a4bc18'},
        #     {'id': '132', 'name': 'YAGMOUR', 'pass': 'ac378556'},
        #     {'id': '133', 'name': 'MARKOVA', 'pass': '08f35d2d'},
        #     {'id': '134', 'name': 'SELÚ', 'pass': 'bf5d3560'},
        #     {'id': '135', 'name': 'PORTSAID', 'pass': '794badd2'},
        #     {'id': '136', 'name': 'DESIDERATA', 'pass': '927ecbdf'},
        #     {'id': '201', 'name': 'PAGO FACIL', 'pass': '1048c0e7'},
        #     {'id': '202', 'name': 'VITAMINA - UMA', 'pass': '094aa6eb'},
        #     {'id': '203', 'name': 'BROER', 'pass': '635b0c2f'},
        #     {'id': '204', 'name': 'PREFIJO', 'pass': '64188c54'},
        #     {'id': '205', 'name': 'GRID', 'pass': '2a739899'},
        #     {'id': '207', 'name': 'LACOSTE', 'pass': 'dfa7939b'},
        #     {'id': '208', 'name': 'TASCANI', 'pass': 'bb1376e4'},
        #     {'id': '209', 'name': 'PENGUIN', 'pass': 'e9209ff1'},
        #     {'id': '210', 'name': 'CREO JOYAS', 'pass': 'd266462a'},
        #     {'id': '211', 'name': 'COMPLOT', 'pass': '750e36f4'},
        #     {'id': '212', 'name': 'SAN ANTONI CLOTHES', 'pass': 'c2ff7088'},
        #     {'id': '213', 'name': 'PRUNE', 'pass': 'b33096d9'},
        #     {'id': '215', 'name': 'URBAN RAIL', 'pass': '0fcffe9e'},
        #     {'id': '216', 'name': 'KOSIUKO', 'pass': '9d4208f9'},
        #     {'id': '217', 'name': 'NARROW', 'pass': 'aaef6349'},
        #     {'id': '218', 'name': 'CITY KIDS', 'pass': '4c161225'},
        #     {'id': '219', 'name': 'PARTEMIA', 'pass': 'f9921ec0'},
        #     {'id': '220', 'name': 'DAVOR', 'pass': 'f8106eb9'},
        #     {'id': '221', 'name': 'BOLIVIA', 'pass': '3213e2b9'},
        #     {'id': '222', 'name': 'KEVINGSTON HOUSE', 'pass': '5b345032'},
        #     {'id': '223', 'name': 'LUZ DE LUNA', 'pass': '3a9f198d'},
        #     {'id': '225', 'name': 'RIP CURL', 'pass': 'd92744ba'},
        #     {'id': '226', 'name': 'GRIMOLDI', 'pass': 'a9bb62ee'},
        #     {'id': '228', 'name': 'BENSIMON', 'pass': 'e010b350'},
        #     {'id': '229', 'name': 'ROUGE', 'pass': '2f7d9152'},
        #     {'id': '233', 'name': 'SPORTLINE PREMIUM', 'pass': '9bc2cc14'},
        #     {'id': '302', 'name': 'ATOMIK', 'pass': '8cd88384'},
        #     {'id': '303', 'name': 'ALMUNDO', 'pass': 'f8867c55'},
        #     {'id': '304', 'name': 'REVER PASS', 'pass': '044d8478'},
        #     {'id': '305', 'name': 'CASASSA & LORENZO', 'pass': '40f657f0'},
        #     {'id': '307', 'name': 'KODAK', 'pass': '5139f425'},
        #     {'id': '308', 'name': 'SOHO', 'pass': 'd884fc42'},
        #     {'id': '309', 'name': 'VACIO 2', 'pass': '1722623c'},
        #     {'id': '310', 'name': 'PURO CUENTO PARTY STORE', 'pass': '87b84b91'},
        #     {'id': '311', 'name': 'MORPH', 'pass': '37d620a5'},
        #     {'id': '313', 'name': 'HOME COLLECTION', 'pass': 'e240b8da'},
        #     {'id': '315', 'name': 'LEF', 'pass': '374cc706'},
        #     {'id': '317', 'name': 'BETOS', 'pass': '82788a4b'},
        #     {'id': '318', 'name': 'MC DONALDS', 'pass': '43e9050b'},
        #     {'id': '320', 'name': 'MOSTAZA', 'pass': '5877c5a9'},
        #     {'id': '321', 'name': 'TERRA DI PASTA', 'pass': '497e9816'},
        #     {'id': '322', 'name': 'LA BRIOCHE DOREE', 'pass': '3036b3e0'},
        #     {'id': '323', 'name': 'QUESTA PIZZA', 'pass': 'bc574032'},
        #     {'id': '32401', 'name': 'DELI RANCH', 'pass': '786829a8'},
        #     {'id': '32402', 'name': 'GREEN & CO', 'pass': '5e8f8097'},
        #     {'id': '32501', 'name': 'AVE CAESAR', 'pass': 'e07260f5'},
        #     {'id': '32502', 'name': 'CHUNGO', 'pass': '18d2c0d8'},
        #     {'id': '32601', 'name': 'LA ESQUINA DE LAS FLORES', 'pass': '751c15ff'},
        #     {'id': '32602', 'name': 'SUBWAY', 'pass': '7bf33b2d'},
        #     {'id': '327', 'name': 'LA CARDEUSE', 'pass': '7c91b593'},
        #     {'id': '329', 'name': 'FARENHEITE', 'pass': '876db303'},
        #     {'id': '330', 'name': 'MUSIMUNDO', 'pass': '9f47669a'},
        #     {'id': '332', 'name': 'EQUUS', 'pass': '2a150ad2'},
        #     {'id': '333', 'name': 'AREA COCOT', 'pass': 'fee2cfad'},
        #     {'id': '334', 'name': 'OPTIPRIX', 'pass': 'd1d3f19f'},
        #     {'id': '335', 'name': 'ADMIT ONE', 'pass': '4742c227'},
        #     {'id': '336', 'name': 'BONAFIDE', 'pass': 'cf7ffac0'},
        #     {'id': '337', 'name': 'SCANDINAVIAN', 'pass': '31f39231'},
        #     {'id': '338', 'name': 'CLUB DEL PELO', 'pass': 'e8c06179'},
        #     {'id': '339', 'name': 'HAIR RECOVERY', 'pass': '5838e47b'},
        #     {'id': '401', 'name': 'PLAYLAND', 'pass': 'd067cdc7'}
        # ]

        # for x in a:
        #     u = User.objects.create(
        #         dni=x['id'],
        #         first_name=x['name'].lower(),
        #         last_name=x['name'].lower(),
        #         type_user='1'
        #     )
        #     u.set_password(x['pass'])
        #     u.save()
        #     l = Local.objects.create(name=x['name'].lower().replace(" ", "_"), owner=u)
        #     print('{}-{}'.format(u, l))

        return redirect(
            'sales_app:r_sales_su',
            local=request.GET.get('local'),
            month=request.GET.get('month'),
            year=request.GET.get('year')
        )
