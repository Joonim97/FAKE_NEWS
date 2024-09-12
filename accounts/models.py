from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    gender_choices = [("M", "남성"), ("F", "여성")]
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30)
    birthday =  models.DateField()
    gender = models.CharField(
        max_length=1, choices=gender_choices, null=True, blank=True
    )
    introduction = models.TextField(blank=True)