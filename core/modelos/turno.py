from django.db import models


class Turno(models.Model):
    nombre_turno = models.CharField(max_length=200, blank=True, null=False)
    nombre = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    cantidad_horas = models.CharField(max_length=300, blank=True, null=False)
    horas_colacion = models.IntegerField(blank=True, null=False)
    termino_turno = models.CharField(max_length=20, blank=True, null=False)
    
    class Meta:
        db_table = 'TURNO'

    def __str__(self):
        return self.nombre_turno