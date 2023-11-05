from django.db import models
from django.core.validators import MinValueValidator  

class TiempoCambio(models.Model):
    #Tiempo de Ajuste entre Patrones de Corte o cambios de sierra  TP
    valor = models.FloatField()
    usuario_crea = models.CharField(max_length=20, blank=True, null=False)
    fecha_crea = models.DateField(auto_now_add=True)
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    Hrs_cambio = models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=False) #TP
    costosobretiempo = models.OneToOneField('CostoSobreTiempo', on_delete=models.CASCADE, verbose_name='Tiempo de Cambio', blank=True, null=False)

    class Meta:
        db_table = 'TIEMPO_CAMBIO'
        
    def __str__(self):
        return f'valor de tiempo cambio = {self.valor}'