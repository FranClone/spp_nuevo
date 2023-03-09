# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Rollizo(models.Model):
    id_rollizo = models.AutoField(primary_key=True)
    nombre_rollizo = models.CharField(max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    descripcion_rollizo = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    id_linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea', db_column='id_linea', blank=True, null=True)
    diametro = models.IntegerField(blank=True, null=True)
    id_largo = models.ForeignKey('RollizoLargo', on_delete=models.CASCADE, verbose_name='Largo', db_column='id_largo', blank=True, null=True)
    usuario_crea = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True, blank=True, null=True)
    id_patron = models.IntegerField(blank=True, null=True)
    clase_diametrica = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'ROLLIZO'

    def __str__(self):
        return self.nombre_rollizo