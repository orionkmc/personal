from django import template
import datetime
register = template.Library()


@register.simple_tag
def validate(user):
    a = datetime.date.today()

    for x in user.employee.all():
        if x.due_date.strftime("%Y-%m-%d") >= a.strftime("%Y-%m-%d"):
            return 'activo'
    return 'vencido'
