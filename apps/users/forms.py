from django import forms
from django.contrib.auth import authenticate
# Apps
# from .models import User


class LoginForm(forms.Form):
    email = forms.CharField(
        label='E-mail',
        required=True,
        widget=forms.TextInput(
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
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError(
                'Los datos de usuario no son correctos'
            )

        return self.cleaned_data
