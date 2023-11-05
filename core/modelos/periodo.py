# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Periodo(models.Model):
    nombre_periodo = models.CharField(max_length=200, blank=True, null=False)
    tipo_periodo = models.ForeignKey('TipoPeriodo', on_delete=models.CASCADE, verbose_name='Tipo de Periodo')
    descripcion_periodo = models.CharField(max_length=300, blank=True, null=True)
    cantidad_periodos = models.IntegerField(blank=True, null=False)
    usuario_crea = models.CharField(max_length=20, blank=True, null=False)
    fecha_crea = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'PERIODO'

    def __str__(self):
        return self.nombre_periodo