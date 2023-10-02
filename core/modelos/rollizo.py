from django.db import models
from django.core.validators import MinValueValidator    

class Rollizo(models.Model):
    nombre_rollizo = models.CharField(max_length=300)
    descripcion_rollizo = models.CharField(max_length=500, blank=True, null=True)
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    diametro =models.FloatField(max_length=10, validators=[MinValueValidator(0)],null=True)
    largo = models.FloatField(max_length=10, validators=[MinValueValidator(0)],null=True)
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    CLASE_DIAMETRICA_CHOICES = []
    for i in range(12, 31, 2):
        CLASE_DIAMETRICA_CHOICES.append((i, i))
    clase_diametrica = models.IntegerField(blank=True, null=True, choices=CLASE_DIAMETRICA_CHOICES)
    eliminado = models.BooleanField(default=False)
    
    def eliminar(self):
        # Marcar el registro como eliminado
        self.eliminado = True
        self.save()

    class Meta:
        db_table = 'ROLLIZO'

    def __str__(self):
        return self.nombre_rollizo                             