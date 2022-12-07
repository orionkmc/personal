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
    observations = models.TextField(verbose_name='Observaciones')

    @property
    def total_nc(self):
        return self.sale_value - self.nc_value

    @property
    def pxt(self):
        return self.quantity_units / self.quantity_tickets

    @property
    def precio_promedio(self):
        return self.sale_value / self.quantity_units

    @property
    def ticket_promedio(self):
        return self.sale_value / self.quantity_tickets
