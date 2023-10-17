# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinValueValidator    

class CostoSobreTiempo(models.Model):
    #suma de las horas extras del equipo 
    costos_horas_extras = models.FloatField(null=True,validators=[MinValueValidator(0)])
    cantidad_horas  = models.FloatField(null=True,validators=[MinValueValidator(0)])
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, verbose_name='Empresa', db_column='rut_empresa', blank=True, null=True)
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'COSTO_SOBRE_TIEMPO'
        
    def __str__(self):
        return 'costo sobre tiempo: ' + str(self.valor)