from django.db import models
from django.core.validators import MinValueValidator                                             
    
class Empaque(models.Model):
    pqte = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    tipo_empaque = models.CharField(max_length=40, null=True, blank=False)
    alto_paquete = models.FloatField(validators=[MinValueValidator(0)], null=True)
    int_paquete = models.FloatField(validators=[MinValueValidator(0)], null=True)
    anc_paquete = models.FloatField(validators=[MinValueValidator(0)], null=True)

    class Meta:
        db_table = 'Paquete'
        
    def __str__(self):
        return str(self.pk)