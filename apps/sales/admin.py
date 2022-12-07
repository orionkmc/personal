from django.contrib import admin
from apps.sales.models import Sales


class SalesAdmin(admin.ModelAdmin):
    list_display = (
        'local', 'date', 'sale_value', 'quantity_units', 'quantity_tickets', 'nc_value', 'can_edit',
    )
    list_filter = ['local__name', 'can_edit']

admin.site.register(Sales, SalesAdmin)
