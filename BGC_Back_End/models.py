from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.hashers import make_password, check_password


class Regulation(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField()
    address = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)


class Graft(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.BinaryField(blank=True)
    purchase_link = models.URLField(blank=True)

    def __str__(self):
        return self.name
