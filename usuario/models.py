# coding=utf-8

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class UserManager(BaseUserManager):
    
    def create_user(self, email, date_of_birth, password=None):
        if not email:
            raise ValueError("Ingrese una dirección de correo")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        user = self.create_user(email, password=password, date_of_birth=date_of_birth)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", max_length=50, unique=True)
    date_of_birth = models.DateField(verbose_name="Fecha de nacimiento")
    is_active = models.BooleanField(default=True, verbose_name="Esta activo") 
    is_admin = models.BooleanField(default=False, verbose_name="Es administrador")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
