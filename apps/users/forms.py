from django import forms
from django.contrib.auth import authenticate
# Apps
# from .models import User


class LoginForm(forms.Form):
    dni = forms.CharField(
        label='E-mail',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'id': 'form1Example1',
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'form1Example2',
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        dni = self.cleaned_data['dni']
        password = self.cleaned_data['password']

        if not authenticate(dni=dni, password=password):
            raise forms.ValidationError(
                'Los datos de usuario no son correctos'
            )

        return self.cleaned_data
