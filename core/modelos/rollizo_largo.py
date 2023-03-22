# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class RollizoLargo(models.Model):
    nombre_largo = models.CharField(max_length=200)
    descripcion_largo = models.CharField(max_length=300, blank=True, null=True)
    largo = models.FloatField()
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'ROLLIZO_LARGO'

    def __str__(self):
        return self.nombre_largo