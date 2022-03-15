# Django
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

# Apps
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    TYPE_USER = [
        ('1', 'Dueño'),
        ('2', 'Gerente'),
        ('3', 'Staff'),
    ]

    email = models.EmailField(unique=True)
    type_user = models.CharField(
        "Tipo de Usuario", max_length=1, choices=TYPE_USER,
        default='3'
    )
    first_name = models.CharField('Nombres', max_length=100)
    last_name = models.CharField('Apellidos', max_length=100)
    phone = models.CharField(
        'Telefono', max_length=100, help_text="809-472-2626", blank=True
    )
    image = models.ImageField('foto', upload_to='media/local/employees')

    #
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'first_name', 'last_name', 'type_user'
    ]

    objects = UserManager()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.email
