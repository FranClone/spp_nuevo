from django.db import models


class StockRollizo(models.Model):
    rollizo = models.ForeignKey('Rollizo', on_delete=models.CASCADE, verbose_name='Rollizo')
    cantidad = models.FloatField()
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    bodega = models.ForeignKey('Bodega', on_delete=models.CASCADE, verbose_name='Bodega')

    class Meta:
        db_table = 'STOCK_ROLLIZO'
        
    def __str__(self):
        return f'Stock de {self.rollizo.nombre_rollizo} en {self.bodega.nombre_bodega} = {self.cantidad}'