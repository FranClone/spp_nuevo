from django.db import models

class MateriaPrima(models.Model):
    """Este modelo define la entidad Materia Prima"""
    
    # Entradas
    #el atributo mas importante en este modelo es la clase_diametrica, la materia prima se clasifica por el numero de buzon, conicidad es la forma del tronco
    nombre= models.CharField(max_length=20, null=False, blank=False)
    volumen_llegada = models.PositiveIntegerField(null=False, blank=False)
    procedencia = models.CharField(max_length=10)
    cantidad = models.PositiveIntegerField(null=False, blank=False)
    largo= models.PositiveIntegerField(null=False, blank=False)
    clase_diametrica= models.PositiveIntegerField(null=False, blank=False) 
    conicidad = models.FloatField(max_length=10)
    tipo_madera = models.CharField(max_length=10)
    # Salidas
    volumen_procesado = models.FloatField(max_length=10)
    inventario_final = models.FloatField(max_length=10)
        
    def __str__(self):
        return f'MateriaPrima {self.nombre}: {self.volumen_llegada} m3'

