from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models

class LawyerRequest(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True,max_length=191)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    specialization = models.CharField(max_length=200)
    experience = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    fee = models.IntegerField()
    about = models.TextField()
    documents = models.FileField(upload_to='documents/', null=True, blank=True)
    picture = models.ImageField(upload_to='lawyer_pics/', null=True, blank=True)  # <-- optional picture
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request: {self.full_name}"


class Lawyer(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True,max_length=191)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    specialization = models.CharField(max_length=200)
    experience = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    fee = models.IntegerField()
    about = models.TextField()
    documents = models.FileField(upload_to='documents/', null=True, blank=True)
    picture = models.ImageField(upload_to='lawyer_pics/', null=True, blank=True)  # <-- optional picture
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

