from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class PatronCorte(models.Model):
    """Este modelo define la entidad Patrón de Corte"""
    
    # Entradas 
    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False, default='')
    nombre = models.CharField(max_length=20, null=False, blank=False)
    descripcion = models.CharField(max_length=20, null=False, blank=False)
    rollizo_id = models.CharField(max_length=10)
    rendimiento = models.FloatField(max_length=5)


    # Salidas
    #patron corte:estrategia para realizar cortes >Utilizado:descartado en la planificacion o utilizado
    utilizado = models.BooleanField()
    eliminado = models.BooleanField(default=False)
    
    def eliminar(self):
        # Marcar el registro como eliminado
        self.eliminado = True
        self.save()

    def __str__(self):
        return f'id {self.codigo}: {self.rendimiento} %'
