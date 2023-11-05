from django.db import models

#Inventario de Materias Primas (rollizo), al inicio de produccion (luego de ser clasificados en buzones) IIR
class StockRollizo(models.Model):
    rollizo = models.ForeignKey('Rollizo', on_delete=models.CASCADE, verbose_name='Rollizo')
    cantidad = models.FloatField()#m3
    usuario_crea = models.CharField(max_length=20, blank=True, null=False)
    fecha_crea = models.DateField(auto_now_add=True)
    bodega = models.ForeignKey('Bodega', on_delete=models.CASCADE, verbose_name='Bodega')
    dias_produccion = models.DateField(null=False)
    Costo_elab = models.FloatField(null=False)
    stock_entrante = models.FloatField(null=False)
    class Meta:
        db_table = 'STOCK_ROLLIZO'
        
    def __str__(self):
        return f'Stock de {self.rollizo.nombre_rollizo} en {self.bodega.nombre_bodega} = {self.cantidad}'