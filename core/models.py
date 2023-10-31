from django.db import models
from django.utils import timezone
from core.modelos.empaque import Empaque
from core.modelos.factura import Factura
from core.modelos.demanda import Demanda
from core.modelos.rendimiento_producto import Rendimiento_Producto

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
    
    def __str__(self):
        return f'Usuario {self.Rut}'
    
    
    #def update_login_time(self):
    #    self.hora_ingreso = timezone.now().time()
    #    self.save()
        
    #def update_logout_time(self):
    #    self.hora_salida = timezone.now().time()
    #    self.save()
    
    
    
class Boletatest(models.Model):
    op = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, null=False, blank=False)
    mercado = models.CharField(max_length=20, null=False, blank=False)
    fecha_emision = models.CharField(max_length=20, null=False, blank=False)
    eta = models.CharField(max_length=20, null=False, blank=False)
    version = models.CharField(max_length=20, null=False, blank=False)
    comentario = models.CharField(max_length=20, null=False, blank=False)
    destino = models.CharField(max_length=20, null=False, blank=False)
    tipo_empaque = models.CharField(max_length=20, null=False, blank=False)
    alto = models.CharField(max_length=20, null=False, blank=False)
    ancho = models.CharField(max_length=20, null=False, blank=False)
    cant_piezas = models.CharField(max_length=20, null=False, blank=False)
    m3 = models.CharField(max_length=20, null=False, blank=False)
    pqte = models.CharField(max_length=20, null=False, blank=False)
    nombreproducto = models.CharField(max_length=20, null=False, blank=False)
    est = models.CharField(max_length=20, null=False, blank=False)
    term = models.CharField(max_length=20, null=False, blank=False)
    calidad = models.CharField(max_length=20, null=False, blank=False)
    fsc = models.CharField(max_length=20, null=False, blank=False)
    espesor = models.CharField(max_length=20, null=False, blank=False)
    ancho = models.CharField(max_length=20, null=False, blank=False)
    largo = models.CharField(max_length=20, null=False, blank=False)
    
    def __str__(self):
        return f'Nombre {self.nombre}'