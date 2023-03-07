# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ProductosEmpresa(models.Model):
    rut_empresa = models.ForeignKey('Empresa', models.DO_NOTHING, verbose_name='Empresa', db_column='rut_empresa')
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, verbose_name='Producto', db_column='id_producto')

    class Meta:
        db_table = 'PRODUCTOS_EMPRESA'
        unique_together = (('rut_empresa', 'id_producto'),)

        
    def __str__(self):
        return f'{self.rut_empresa} - {self.id_producto}'
