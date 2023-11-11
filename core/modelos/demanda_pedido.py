from django.db import models
from .pedidos import Pedido
from .demanda import Demanda

class Demanda_Producto(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, verbose_name='Pedido')
    demanda = models.ForeignKey('Demanda', on_delete=models.CASCADE, verbose_name='Demanda')


    class Meta:
        db_table = 'Demanda_Producto'