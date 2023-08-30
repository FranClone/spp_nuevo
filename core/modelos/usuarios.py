from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    Rut = models.CharField(primary_key=True,max_length=20, null=False, blank=False)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    apellido = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)
    telefono = models.CharField(max_length=20, null=False, blank=False)
    empresa = models.CharField(max_length=20, null=False, blank=False)
    rol = models.CharField(max_length=20, null=False, blank=False)
    turno = models.CharField(max_length=20, null=False, blank=False) 
    hora_ingreso = models.TimeField(null=False,blank=False)
    hora_salida = models.TimeField(null=False,blank=False)
    contraseña = models.CharField(max_length=50, null=False, blank=False)
    def __str__(self):
        return f'Usuario {self.Rut}%'

    #def update_login_time(self):
    #    self.hora_ingreso = timezone.now().time()
    #    self.save()

    #def update_logout_time(self):
    #    self.hora_salida = timezone.now().time()
    #    self.save()
    
    """Este modelo define la entidad Usuario
    
    def __str__(self):
        return f'Usuario {self.Rut}%'

    """
