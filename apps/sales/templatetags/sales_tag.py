from django import template
from apps.sales.models import Sales
# import datetime
register = template.Library()


@register.simple_tag
def total_nc(sale):
    if sale.exists():
        return '{0:.2f}'.format(sale[0].sale_value - sale[0].nc_value)
    return '-'


@register.simple_tag
def pxt(sale):
    if sale.exists():
        return '{0:.2f}'.format(sale[0].quantity_units / sale[0].quantity_tickets)
    return '-'


@register.simple_tag
def precio_promedio(sale):
    if sale.exists():
        return '{0:.2f}'.format(sale[0].sale_value / sale[0].quantity_units)
    return '-'


@register.simple_tag
def ticket_promedio(sale):
    if sale.exists():
        return '{0:.2f}'.format(sale[0].sale_value / sale[0].quantity_tickets)
    return '-'


@register.simple_tag
def days_locked(local, d, month, year, day):
    s = Sales.objects.filter(local__slug=local, date__day=d, date__month=month, date__year=year)
    if not s.exists() or len(s.filter(can_edit=True)) > 0:
        if day == d:
            return 'bg-black text-white'
        else:
            return 'bg-green-500 hover:bg-green-600'

    if day == d:
            return 'bg-black text-white'
    else:
        return 'bg-indigo-600 hover:bg-indigo-700'


@register.simple_tag
def months_locked(local, month, year):
    s = Sales.objects.filter(local__slug=local, date__month=month, date__year=year, can_edit=True)

    if len(s) > 0:
        return 'bg-green-500 hover:bg-green-600'
    return 'bg-indigo-600 hover:bg-indigo-700'
