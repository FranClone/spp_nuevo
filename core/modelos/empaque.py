from django.db import models
from django.core.validators import MinValueValidator                                             
    
class Empaque(models.Model):
    pqte = models.DecimalField(max_digits=10, decimal_places=3, null=False)
    tipo_empaque = models.CharField(max_length=40, null=False, blank=False)
    alto_paquete = models.FloatField(validators=[MinValueValidator(0)], null=False)
    int_paquete = models.FloatField(validators=[MinValueValidator(0)], null=False)
    anc_paquete = models.FloatField(validators=[MinValueValidator(0)], null=False)

    class Meta:
        db_table = 'Paquete'
        
    def __str__(self):
        return str(self.pk)