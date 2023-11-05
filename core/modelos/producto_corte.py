from django.db import models


class ProductoCorte(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, verbose_name='Producto')
    patron = models.ForeignKey('PatronCorte', on_delete=models.CASCADE, verbose_name='Patrón de Corte')
    cantidad_producto = models.IntegerField(blank=True, null=False)
    descripcion_corte = models.CharField(max_length=200, blank=True, null=False)
    usuario_crea = models.CharField(max_length=20, blank=True, null=False)
    fecha_crea = models.DateField(auto_now_add=True, blank=True, null=False)
    rollizo = models.ForeignKey('Rollizo', on_delete=models.CASCADE, db_column='id_rollizo', blank=True, null=False)

    class Meta:
        db_table = 'PRODUCTO_CORTE'

    def __str__(self):
        return self.descripcion_corte