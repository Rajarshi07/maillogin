from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    '''
        Custom User Model
    '''
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class WhitelistDomain(models.Model):
    domain = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return self.domain

class BlacklistDomain(models.Model):
    domain = models.CharField(max_length=100, primary_key=True)
    def __str__(self):
        return self.domain

