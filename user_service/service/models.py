from django.db import models


# Site user model
class User(models.Model):
    login = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=35)
