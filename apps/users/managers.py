# Django
from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    def _create_user(
        self,
        dni,
        password,
        is_staff,
        is_superuser,
        is_active,
        **extra_fields
    ):
        user = self.model(
            dni=dni,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, password=None, **extra_fields):
        return self._create_user(
            password, False, False, True, **extra_fields
        )

    def create_superuser(self, dni, password=None, **extra_fields):
        return self._create_user(
            dni, password, True, True, True, **extra_fields
        )
