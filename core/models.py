from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)

    def is_administrator(self):
        return self.role == 'administrator'
    
    def is_cliente(self):
        return self.role == 'cliente'
