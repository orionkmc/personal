from django import forms
# Apps
from apps.users.models import User
from apps.locals.models import Local, Manager, Employee


class ManagerForm(forms.Form):
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': '',
                'class': 'form-control',
            }
        )
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'form-control',
            }
        )
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'form-control',
            }
        )
    )

    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': '',
                'class': 'form-control',
            }
        )
    )

    image = forms.ImageField(
        required=True
    )

    def save(self, local, type_user, commit=True):

        data = self.cleaned_data
        user, created = User.objects.get_or_create(
            email=data['email'],
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone': data['phone'],
                'image': data['image'],
                'type_user': 2,

            },
        )
        if type_user == 'manager':
            if created or not Manager.objects.filter(local=Local.objects.get(slug=local), manager=user).exists():
                Manager.objects.create(local=Local.objects.get(slug=local), manager=user)
        elif type_user == 'employee':
            if created or not Employee.objects.filter(local=Local.objects.get(slug=local), employee=user).exists():
                Employee.objects.create(local=Local.objects.get(slug=local), employee=user)


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'image', )
