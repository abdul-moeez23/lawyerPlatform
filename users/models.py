from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('lawyer', 'Lawyer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)


# =========================
# LOOKUP TABLES
# =========================

class City(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name


class Court(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self): return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self): return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    def __str__(self): return self.name


class FeeBand(models.Model):
    label = models.CharField(max_length=100)
    min_fee = models.IntegerField(default=0)
    max_fee = models.IntegerField(default=0)
    def __str__(self): return self.label


class Language(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name