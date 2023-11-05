from django.db import models
from .producto_medida import ProductoMedida
#Inventario ya producido del producto IIP
#Valorización del Inventarioa VI
#Costo de almacenacimiento de PT X CBM CI
class StockProducto(models.Model):
    bodega = models.ForeignKey('Bodega', on_delete=models.CASCADE, verbose_name='Bodega')
    producto_medida = models.ForeignKey('ProductoMedida', on_delete=models.CASCADE)
    #producto_key = models.CharField(max_length=300, null=True)
    cantidad_m3 = models.FloatField(null=False)
    fecha_crea = models.DateField(auto_now_add=True)
    usuario_crea = models.CharField(max_length=20, blank=True, null=False)
    valor_inventario = models.FloatField(null=True,max_length=10) #USD/M3 VI
    costo_almacenamiento = models.FloatField(null=True,max_length=10) #CI
    class Meta:
        db_table = 'STOCK_PRODUCTO'
        
    def __str__(self):
        return f'Stock de  en {self.bodega.nombre_bodega} = {self.cantidad_m3}'