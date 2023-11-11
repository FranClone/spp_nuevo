from django.db import models


class Produccion(models.Model):
    nombre = models.CharField(max_length=20)
    costos_sobretiempo = models.PositiveIntegerField(null=False, blank=False)
    produccion_horas_extras = models.PositiveIntegerField(null=False, blank=False)
    fecha_produccion = models.DateField(auto_now_add=True)
    cantidad = models.ForeignKey('DetallePedido', on_delete=models.CASCADE)

    class Meta:
        db_table = 'PRODUCCION'

    def __str__(self):
        return self.nombre