# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinValueValidator    

class CostoRollizo(models.Model):
    #*Costos de procesos por M3 por Rollizo X Linea CR
    rollizo = models.ForeignKey('rollizo', on_delete=models.CASCADE, verbose_name='rollizo')
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, verbose_name='Empresa', db_column='rut_empresa')
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    nombre_costo = models.CharField(null=False,max_length=200)
    valor_m3 = models.FloatField(null=False,validators=[MinValueValidator(0)]) # Costo usd/m3
    fecha_crea = models.DateField(auto_now_add=True)
    usuario_crea = models.CharField(max_length=20, blank=True, null=False)


    class Meta:
        db_table = 'COSTO_ROLLIZO'

    def __str__(self):
        return self.nombre_costo