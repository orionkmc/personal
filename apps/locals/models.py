# Django
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils import timezone
from datetime import date, timedelta


class Local(models.Model):
    logo = models.ImageField('logo', upload_to='media/local')
    name = models.CharField('Nombre', max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Dueño')
    phone = models.CharField('Telefono', max_length=100, help_text="809-472-2626", blank=True)

    def __str__(self):
        return "{}".format(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Local, self).save(*args, **kwargs)

    def admin_thumbnail(self):
        return mark_safe('<img src="/%s" width="140" />' % self.logo)
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True


class Manager(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, verbose_name='Local')
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Gerente', related_name='manager'
    )

    def __str__(self):
        return "{}".format(self.manager.get_full_name())


class Employee(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, verbose_name='Local')
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Empleado', related_name='employee'
    )
    due_date = models.DateField(verbose_name='Fecha de vencimiento', default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.due_date = date.today() + timedelta(30)
        return super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.employee.get_full_name())
