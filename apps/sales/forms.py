from django import forms
from apps.sales.models import Sales


class SalesForm(forms.ModelForm):

    class Meta:
        model = Sales
        fields = ('sale_value', 'quantity_units', 'quantity_tickets', 'nc_value', 'observations')

        widgets = {
            'sale_value': forms.NumberInput(
                attrs={
                    'class': 'mt-1 block w-64 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                    'form': "sale_day_form"
                }
            ),
            'quantity_units': forms.NumberInput(
                attrs={
                    'class': 'mt-1 block w-64 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                    'form': "sale_day_form"
                }
            ),
            'quantity_tickets': forms.NumberInput(
                attrs={
                    'class': 'mt-1 block w-64 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                    'form': "sale_day_form"
                }
            ),
            'nc_value': forms.NumberInput(
                attrs={
                    'class': 'mt-1 block w-64 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                    'form': "sale_day_form"
                }
            ),
            'observations': forms.Textarea(
                attrs={
                    'class': 'block w-full max-w-lg rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                    'form': "sale_day_form",
                    'rows': "3"
                }
            ),
        }
