from django.db import models
from .patron_corte import PatronCorte
from django.core.validators import MinValueValidator   
class Producto(models.Model):
    """Este modelo define la entidad Producto"""
    
    # Entradas
    orden_producto = models.CharField(max_length=20, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=20, null=False, blank=False)
    descripcion = models.CharField(max_length=100, null=False, blank=False)
    largo =  models.FloatField( validators=[MinValueValidator(0)],null=True, blank=False)
    ancho =  models.FloatField(validators=[MinValueValidator(0)],null=True, blank=False)
    alto = models.FloatField(validators=[MinValueValidator(0)],null=True, blank=False)
    inventario_inicial = models.FloatField(max_length=10)
    valor_inventario = models.FloatField(max_length=10)
    costo_almacenamiento = models.FloatField(max_length=10)
    #Foranea rollizo
    nombre_rollizo = models.ForeignKey('Rollizo', on_delete=models.CASCADE, verbose_name='Rollizo')
    # Salidas
    #volumen_obtenido = models.FloatField(max_length=10)
    inventario_final = models.FloatField(max_length=10)
    patron_corte = models.ManyToManyField(PatronCorte)   
    #Linea de corte                                                  
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    def __str__(self):
        return f' {self.nombre} '

