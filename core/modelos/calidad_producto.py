from django.db import models


class CalidadProducto(models.Model):
    nombre_calidad = models.CharField(max_length=200)
    usuario_crea = models.CharField(max_length=20)
    fecha_crea = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'CALIDAD_PRODUCTO'

    def __str__(self):
        return self.nombre_calidad