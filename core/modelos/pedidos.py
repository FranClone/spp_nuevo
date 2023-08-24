from django.db import models

class Pedido(models.Model):
    """Este modelo define la entidad Pedido"""
    
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


    def __str__(self):
        return f"Pedido {self.codigo}: Fecha Entrega: {self.fecha_entrega} - {self.estado}"
