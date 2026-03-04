from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.email}, {self.first_name}, {self.last_name}'


class Order(models.Model):
    name = models.CharField(max_length=500)