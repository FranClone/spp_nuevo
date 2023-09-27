from django.db import models
from .producto import Producto
from datetime import datetime

class Pedido(models.Model):
    """Este modelo define la entidad Pedido"""
    OPCION_PRIORIDAD= [
    ('', 'Seleccione una opción'), 
    ('bajo', 'Bajo'),
    ('mediano', 'Mediano'),
    ('alto', 'Alto'),
    ]
    
    OPCION_ESTADO= [
    ('', 'Seleccione una opción'),
    ('pendiente', 'Pendiente'),
    ('en proceso', 'En Proceso'),
    ('completado', 'Completado'),
    ]
    
    # OPCION_PRODUCCION= [
    # ('', 'Seleccione una opción'),
    # ('grueso', 'Grueso'),
    # ('delgado', 'Delgado'),
    # ]
    
    # Entradas
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, verbose_name='Cliente')
    fecha_produccion = models.DateField(null=False, blank=False)
    fecha_entrega = models.DateField(null=False, blank=False )
    orden_interna = models.CharField(max_length=20, null=False, blank=False)
    comentario = models.CharField(max_length=200, null=False, blank=False, default='Sin comentario')
    producto = models.ManyToManyField(Producto, through='DetallePedido')
    prioridad = models.CharField(max_length=20,null=True, blank=False,choices=OPCION_PRIORIDAD, default='')
    version = models.PositiveIntegerField(null=False, blank=False)
    #porcentaje_avance = models.FloatField(max_length=5)
    #cantidad_producida = models.PositiveIntegerField(null=False, blank=False)
    
    # Salidas
    estado = models.CharField(max_length=20, null=True, blank=False,choices=OPCION_ESTADO, default='')

    def __str__(self):
        return f"Pedido {self.orden_interna}: Fecha Entrega: {self.fecha_entrega} - {self.estado}"
    

# class Pedido_Producto(models.Model):
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='bcs')
#     pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='bcs')

#     def __str__(self): return str(self.pedido)