from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    apellido = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)
    Rut = models.CharField(primary_key=True,max_length=20, null=False, blank=False)
    telefono = models.CharField(max_length=20, null=False, blank=False)
    empresa = models.CharField(max_length=20, null=False, blank=False)
    rol = models.CharField(max_length=20, null=False, blank=False)
    turno = models.CharField(max_length=20, null=False, blank=False) 
    hora_ingreso = models.TimeField(null=False,blank=False)
    hora_salida = models.TimeField(null=False,blank=False)
    contraseña = models.CharField(max_length=50, null=False, blank=False)

    def str(self):
        return f'Producto {self.Rut}'

    #def update_login_time(self):
    #    self.hora_ingreso = timezone.now().time()
    #    self.save()

    #def update_logout_time(self):
    #    self.hora_salida = timezone.now().time()
    #    self.save()