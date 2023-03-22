# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Rollizo(models.Model):
    nombre_rollizo = models.CharField(max_length=300)
    descripcion_rollizo = models.CharField(max_length=500, blank=True, null=True)
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    diametro = models.IntegerField()
    rollizo_largo = models.ForeignKey('RollizoLargo', on_delete=models.CASCADE, verbose_name='Largo')
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    id_patron = models.IntegerField(blank=True, null=True)
    clase_diametrica = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ROLLIZO'

    def __str__(self):
        return self.nombre_rollizo