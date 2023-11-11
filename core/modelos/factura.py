
from django.db import models
from django.core.validators import MinValueValidator                                             
    
class Factura(models.Model):
    FSC = models.CharField(max_length=40, null=True, blank=False)
    esp_fact = models.FloatField(validators=[MinValueValidator(0)], null=False)
    anc_fact = models.FloatField(validators=[MinValueValidator(0)], null=False)
    lar_fact = models.FloatField(validators=[MinValueValidator(0)], null=False)
    class Meta:
        db_table = 'Factura'

    def __str__(self):
        return str(self.pk)