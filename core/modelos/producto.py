from django.db import models

class Producto(models.Model):
    """Este modelo define la entidad Producto"""
    
    # Entradas
    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=20, null=False, blank=False)
    descripcion = models.CharField(max_length=100, null=False, blank=False)
    largo = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    ancho = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)    
    alto = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    demanda = models.CharField(max_length=100, null=False, blank=False)
    inventario_inicial = models.FloatField(max_length=10)
    valor_inventario = models.FloatField(max_length=10)
    costo_almacenamiento = models.FloatField(max_length=10)
    
    # Salidas
    volumen_obtenido = models.FloatField(max_length=10)
    inventario_final = models.FloatField(max_length=10)
    
    def __str__(self):
        return f'Producto {self.codigo}: {self.descripcion}'

