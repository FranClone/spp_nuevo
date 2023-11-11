from django.db import models


class InvInicialRollizo(models.Model):
    nombre_inventario = models.CharField(max_length=300)
    descripcion_inventario = models.CharField(max_length=500, blank=True, null=True)
    diametro = models.FloatField()
    cant_m3 = models.FloatField()
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    bodega = models.ForeignKey('Bodega', on_delete=models.CASCADE, verbose_name='Bodega')

    class Meta:
        db_table = 'INV_INICIAL_ROLLIZO'

    def __str__(self):
        return self.nombre_inventario