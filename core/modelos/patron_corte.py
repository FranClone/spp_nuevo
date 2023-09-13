from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class PatronCorte(models.Model):
    """Este modelo define la entidad Patrón de Corte"""
    
    # Entradas 
    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False, default='')
    nombre = models.CharField(max_length=20, null=False, blank=False)
    descripcion = models.CharField(max_length=20, null=False, blank=False)
    rendimiento = models.FloatField(max_length=5)
    velocidad_linea = models.FloatField()
    setup_time = models.FloatField()
    lead_time = models.FloatField()

    # Salidas
    #patron corte:estrategia para realizar cortes >Utilizado:descartado en la planificacion o utilizado
    utilizado = models.BooleanField()
    producto_asociado = models.CharField(max_length=20, null=False, blank=False, default='')

    def __str__(self):
        return f'Patrón de corte {self.codigo}: {self.rendimiento} %'
