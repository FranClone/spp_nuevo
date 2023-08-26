from django.db import models

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
    
    # Entradas
    cliente = models.CharField(max_length=50, null=False, blank=False)
    fecha_entrega = models.DateField(null=False, blank=False)
    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False)
    comentario = models.CharField(max_length=200, unique=True, null=False, blank=False, default='Sin comentario')
    nombre = models.CharField(max_length=20, null=False, blank=False)
    producto = models.CharField(max_length=20, null=False, blank=False)
    cantidad = models.PositiveIntegerField(null=False, blank=False)
    prioridad = models.IntegerField(null=False, blank=False)
    linea_produccion = models.CharField(max_length=20, null=False, blank=False)
    
    #porcentaje_avance = models.FloatField(max_length=5)
    #cantidad_producida = models.PositiveIntegerField(null=False, blank=False)
    
    # Salidas
    estado = models.CharField(max_length=20, null=False, blank=False)

    """