from django.db import models


class StockProducto(models.Model):
    bodega = models.ForeignKey('Bodega', on_delete=models.CASCADE, verbose_name='Bodega')
   # detalle = models.ForeignKey('DetallePedido', on_delete=models.CASCADE, verbose_name='DetallePedido')
    producto_key = models.CharField(max_length=300, null=True)
    cantidad_m3 = models.FloatField()
    fecha_crea = models.DateField(auto_now_add=True)
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'STOCK_PRODUCTO'
        
    def __str__(self):
        return f'Stock de {self.producto.nombre_producto} en {self.bodega.nombre_bodega} = {self.cantidad_m3}'