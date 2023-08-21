from django.db import models

class MateriaPrima(models.Model):
    """Este modelo define la entidad Materia Prima"""
    
    # Entradas
    numero_buzon = models.IntegerField()
    tipo_madera = models.CharField(max_length=10)
    clase_diametrica = models.CharField(max_length=10)
    largo = models.FloatField(max_length=10)
    cantidad = models.FloatField(max_length=10)
    conicidad = models.FloatField(max_length=10)
    linea_produccion = models.CharField(max_length=10)
    costo_almacenamiento = models.FloatField(max_length=10) # obviar por el momento
    inventario_inicial = models.FloatField(max_length=10)
    
    # Salidas
    volumen_procesado = models.FloatField(max_length=10)
    inventario_final = models.FloatField(max_length=10)
        
    def __str__(self):
        return f'Buzón {self.numero_buzon}: {self.cantidad} m3'

