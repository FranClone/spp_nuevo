from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import validate_rut

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=20, unique=True)
    rut_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, db_column='rut_empresa', blank=True, null=True)
    
    class Meta:
        app_label = 'core'

    def __str__(self):
        return self.user.username
    
    def clean(self):
        try:
            validate_rut(self.rut)
        except ValidationError as e:
            raise ValidationError({'rut': e})
