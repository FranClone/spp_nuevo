from django.db import models
from .patron_corte import PatronCorte
from .medida import Medida
from django.core.validators import MinValueValidator   
class Producto(models.Model):
    """Este modelo define la entidad Producto"""
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, db_column='rut_empresa')
    nombre_rollizo = models.ForeignKey('Rollizo', on_delete=models.CASCADE, verbose_name='Rollizo')
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    patron_corte = models.ManyToManyField(PatronCorte)  
    medida = models.ManyToManyField(
        Medida,
        through='ProductoMedida') # Campos para enlazar con el modelo intermedio
    
    # Entradas
    orden_producto = models.CharField(max_length=20, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=20, null=False, blank=False)
    descripcion = models.CharField(max_length=100, null=False, blank=False)
    inventario_inicial = models.FloatField(max_length=10)
    # Salidas
    #volumen_obtenido = models.FloatField(max_length=10)
    inventario_final = models.FloatField(max_length=10)
     
    #Linea de corte                                                  
    
    eliminado = models.BooleanField(default=False)
    
    def eliminar(self):
        # Marcar el registro como eliminado
        self.eliminado = True
        self.save()
        
    def __str__(self):
        return f' {self.nombre} '

