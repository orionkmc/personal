from django.db import models
from apps.locals.models import Local


class Sales(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, verbose_name='Local')
    date = models.DateField(verbose_name='Fecha')
    can_edit = models.BooleanField(verbose_name='¿Puede Editar?', default=True)

    sale_value = models.FloatField(verbose_name='Valor Venta')
    quantity_units = models.FloatField(verbose_name='Cantidad Unidades')
    quantity_tickets = models.FloatField(verbose_name='Cantidad Tickets')
    nc_value = models.FloatField(verbose_name='Valor NC')
    observations = models.TextField(verbose_name='Observaciones', null=True, blank=True)

    @property
    def total_nc(self):
        try:
            return self.sale_value - self.nc_value
        except ZeroDivisionError:
            return 0

    @property
    def pxt(self):
        try:
            return self.quantity_units / self.quantity_tickets
        except ZeroDivisionError:
            return 0

    @property
    def precio_promedio(self):
        try:
            return self.sale_value / self.quantity_units
        except ZeroDivisionError:
            return 0

    @property
    def ticket_promedio(self):
        try:
            return self.sale_value / self.quantity_tickets
        except ZeroDivisionError:
            return 0


class ExcelSales(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, verbose_name='Local', related_name='exel')
    date = models.DateField(verbose_name='Fecha')
    url = models.CharField('Excel', max_length=255)
