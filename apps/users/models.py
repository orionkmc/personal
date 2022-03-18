# Django
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.safestring import mark_safe

# Apps
from apps.users.managers import UserManager

# Other
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File


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
    image = models.ImageField('foto', upload_to='media/user/employees')
    qr = models.ImageField(upload_to='media/user/qrcode', blank=True)
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

    def qr_thumbnail(self):
        print(self.qr)
        if self.qr:
            return mark_safe('<img src="/%s" width="140" />' % self.qr)
        return '-'
    qr_thumbnail.short_description = 'Qr'
    qr_thumbnail.allow_tags = True

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            url = 'http://personal.devotoshopping.com.ar/{}'.format(self.email)
            qrcode_img = qrcode.make(url)
            canvas = Image.new("RGB", (400, 400), "white")
            ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            buffer = BytesIO()
            canvas.save(buffer, "PNG")
            self.qr.save('qr.png', File(buffer), save=False)
            canvas.close()
        return super(User, self).save(*args, **kwargs)
