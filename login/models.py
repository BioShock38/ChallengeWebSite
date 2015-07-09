from django.db import models

from django.contrib.auth.models import User

class Challenger(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
