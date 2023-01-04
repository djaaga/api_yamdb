from enum import Enum

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user


class UserRole(Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    @staticmethod
    def get_max_length():
        max_length = max(len(role.value) for role in UserRole)
        return max_length

    @staticmethod
    def get_all_roles():
        return tuple((r.value, r.name) for r in UserRole)


class User(AbstractUser):
    USERNAME_VALIDATOR = RegexValidator(r'^[\w.@+-]+\Z')
    bio = models.TextField(
        'Дополнительная информация',
        blank=True,
    )
    username = models.CharField(validators=[USERNAME_VALIDATOR],
                                max_length=150, unique=True)
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(blank=True, max_length=124)
    confirmation_code = models.CharField(max_length=120, default='000000')
    role = models.CharField(
        max_length=UserRole.get_max_length(),
        choices=UserRole.get_all_roles(),
        default=UserRole.USER.value
    )
    objects = CustomUserManager()

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username
