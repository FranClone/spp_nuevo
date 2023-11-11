from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from core.validators import validate_rut
from core.modelos.empresa import Empresa


class UserProfile(AbstractUser):
    Roles = [
    ('','Seleccione una opcion'),
    ('ADMINISTRADOR', 'Administrador'),
    ('PLANIFICADOR', 'Planificador'),
    ('BETECH', 'Betech'),
    ]
    rut = models.CharField(unique=True, max_length=20)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column='rut_empresa', null=True)
    roles = models.CharField(max_length=20, null=True, blank=False,choices=Roles, default='')

    def __str__(self):
        return self.username

    def clean(self):
        try:
            validate_rut(self.rut)
        except ValidationError as e:
            raise ValidationError({'rut': e})
