# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DetallePedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, verbose_name='Pedido')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, verbose_name='Producto')
    detalle_producto = models.CharField(max_length=300)
    volumen_producto = models.CharField(max_length=10)
    fecha_entrega = models.DateField()
    estado_pedido_linea = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'DETALLE_PEDIDO'
        
    def __str__(self):
        return self.detalle_producto
