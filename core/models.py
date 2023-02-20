from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=20, unique=True)
    rut_empresa = models.CharField(max_length=20)
    class Meta:
        app_label = 'core'