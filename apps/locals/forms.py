from django import forms
from django.core.exceptions import ValidationError
# Apps
from apps.users.models import User
from apps.locals.models import Local, Manager, Employee


class ManagerForm(forms.Form):
    dni = forms.CharField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.CharField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': "form-control",
                'aria-describedby': "passHelp",
            }
        )
    )

    password_again = forms.CharField(
        label='Password Again',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password',
                'class': "form-control",
                'aria-describedby': "passHelp",
            }
        )
    )

    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise ValidationError('Passwords do not match')
        return password_again

    def save(self, local, type_user, commit=True):
        data = self.cleaned_data

        user, created = User.objects.update_or_create(
            dni=data['dni'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone': data['phone'],
                'image': data['image'],
                'type_user': type_user,
            },
        )
        if created:
            user.set_password(data['password'])
            user.save()

        if type_user == 2:
            if created or not Manager.objects.filter(local=Local.objects.get(slug=local), manager=user).exists():
                Manager.objects.create(local=Local.objects.get(slug=local), manager=user)
                

class EmployeeForm(forms.Form):
    dni = forms.CharField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.CharField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def save(self, local, type_user, commit=True):
        data = self.cleaned_data

        user, created = User.objects.update_or_create(
            dni=data['dni'],
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'phone': data['phone'],
                'image': data['image'],
                'type_user': type_user,
            },
        )

        if type_user == 3:
            if created or not Employee.objects.filter(local=Local.objects.get(slug=local), employee=user).exists():
                Employee.objects.create(local=Local.objects.get(slug=local), employee=user)


class ManagerUpdateForm(forms.ModelForm):
    password_again = forms.CharField(
        label='Password Again',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password',
                'class': "form-control",
                'aria-describedby': "passHelp",
            }
        )
    )

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise ValidationError('Passwords do not match')
        return password_again

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password', 'image', )

        widgets = {
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ManagerUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False

    def _save(self):
        u = User.objects.get(pk=self.instance.pk)
        u.email = self.cleaned_data['email']
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.phone = self.cleaned_data['phone']
        if len(self.cleaned_data["password"]) > 0:
            u.set_password(self.cleaned_data["password"])
        u.save()

class EmployeeUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'image', )

        widgets = {
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
