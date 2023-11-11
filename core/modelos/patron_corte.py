from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class PatronCorte(models.Model):
    """Este modelo define la entidad Patrón de Corte"""
   #Rendimiento del Patron de corte RE 

    rollizo = models.ForeignKey('Rollizo', on_delete=models.CASCADE, verbose_name='Rollizo')
    codigo = models.CharField(max_length=20, unique=False, null=False, blank=False, default='')
    nombre = models.CharField(max_length=20, null=False, blank=False)
    descripcion = models.CharField(max_length=20, null=True, blank=False)
    rendimiento = models.FloatField(max_length=5, null=False,validators=[MinValueValidator(0)]) #RE
   #patron corte:estrategia para realizar cortes >Utilizado:descartado en la planificacion o utilizado

    utilizado = models.BooleanField()
    eliminado = models.BooleanField(default=False)


    # Salidas
 
    
    def eliminar(self):
        # Marcar el registro como eliminado
        self.eliminado = True
        self.save()

    def __str__(self):
        return f'id {self.codigo}: {self.rendimiento} %'
    #rollizo = models.CharField(max_length=10)

    #velocidad_linea = models.FloatField()
    #setup_time = models.FloatField()
    #lead_time = models.FloatField()