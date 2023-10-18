# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinValueValidator                                             
from .producto import Producto    
from .medida import Medida
class ProductoMedida(models.Model):
    #Demanda en m3  en verde D
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, verbose_name='Producto')
    medida = models.ForeignKey('Medida', on_delete=models.CASCADE, verbose_name='Medida')
   
    class Meta:
        db_table = 'producto_medida'
        
    def __str__(self):
        return self.id
