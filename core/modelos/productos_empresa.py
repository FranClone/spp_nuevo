# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ProductosEmpresa(models.Model):
    id_pempresa = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE, db_column='id_producto')
    rut_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, db_column='rut_empresa')

    class Meta:
        db_table = 'PRODUCTOS_EMPRESA'
        unique_together = (('id_producto', 'rut_empresa'),)

    def __str__(self):
        return f'{self.id_producto} de {self.rut_empresa}'
