from django.db import models
from .pedidos import Pedido
class Demanda(models.Model):
    pedido = models.ManyToManyField(Pedido, through='Demanda_Producto')
    Medida_Producto_id = models.PositiveIntegerField(null=False)
    dias_produccion = models.DateField(null=False)
    Pqtes_Solicitados = models.PositiveIntegerField(null=False)
    Pqtes_dia = models.PositiveIntegerField(null=False)
    M3 = models.FloatField(null=False)
    class Meta:
        db_table = 'Demanda'
        
    def __str__(self):
        return self.dias_produccion
