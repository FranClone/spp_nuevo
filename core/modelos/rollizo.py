from django.db import models


class Rollizo(models.Model):
    nombre_rollizo = models.CharField(max_length=300)
    descripcion_rollizo = models.CharField(max_length=500, blank=True, null=True)
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    diametro = models.IntegerField()
    largo = models.ForeignKey('RollizoLargo', on_delete=models.CASCADE, verbose_name='Largo')
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    CLASE_DIAMETRICA_CHOICES = []
    for i in range(12, 31, 2):
        CLASE_DIAMETRICA_CHOICES.append((i, i))
    clase_diametrica = models.IntegerField(blank=True, null=True, choices=CLASE_DIAMETRICA_CHOICES)

    class Meta:
        db_table = 'ROLLIZO'

    def __str__(self):
        return self.nombre_rollizo