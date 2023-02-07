from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=20)
    
    def validate_rut(value):
        rut = str(value)
        rut = rut.replace(".", "").replace("-", "")
        if not rut.isdigit():
            raise ValidationError('El RUT solo puede contener números y un guión')
        if len(rut) < 8:
            raise ValidationError('El RUT es demasiado corto')
        rev = map(int, reversed(str(rut[:-1])))
        sum = 0
        for i, x in enumerate(rev):
            if i == 8:
                break
            sum += x * (i + 2)
        v = 11 - sum % 11
        if v == 10:
            digit = 'k'
        elif v == 11:
            digit = '0'
        else:
            digit = str(v)
        if digit.lower() != rut[-1].lower():
            raise ValidationError('El dígito verificador es incorrecto')
        
    class Meta:
        app_label = 'core'