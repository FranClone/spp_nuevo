# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=300, verbose_name='Producto')
    descripcion_producto = models.CharField(max_length=500, blank=True, null=True)
    espesor_producto = models.FloatField(blank=True, null=True)
    ancho_producto = models.FloatField(blank=True, null=True)
    largo_producto = models.FloatField(blank=True, null=True)
    usuario_crea = models.CharField(max_length=20)
    fecha_crea = models.DateField(auto_now_add=True)
    calidad_producto = models.ForeignKey('CalidadProducto', on_delete=models.CASCADE, verbose_name='Calidad de Producto')

    class Meta:
        db_table = 'PRODUCTO'
        
    def __str__(self):
        return self.nombre_producto