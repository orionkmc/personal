# Generated by Django 3.2 on 2022-12-06 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locals', '0002_auto_20220422_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('sale_value', models.FloatField(verbose_name='Valor Venta')),
                ('quantity_units', models.FloatField(verbose_name='Cantidad Unidades')),
                ('quantity_tickets', models.FloatField(verbose_name='Cantidad Tickets')),
                ('nc_value', models.FloatField(verbose_name='Valor NC')),
                ('observations', models.FloatField(verbose_name='Observaciones')),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locals.local', verbose_name='Local')),
            ],
        ),
    ]
