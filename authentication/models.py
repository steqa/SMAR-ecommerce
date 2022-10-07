from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    fio = models.CharField(_('ФИО'), max_length=200)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []