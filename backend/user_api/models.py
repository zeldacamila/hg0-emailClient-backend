from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(verbose_name='emails', unique=True, max_length=255)
