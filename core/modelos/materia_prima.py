from django.db import models

class MateriaPrima(models.Model):
    numero_buzon = models.IntegerField()
    tipo_madera = models.CharField(max_length=100)
    clase_diametrica = models.CharField(max_length=100)
    longitud = models.FloatField()
    cantidad = models.FloatField()
        
    def __str__(self):
        return f'Buzón {self.numero_buzon}: {self.tipo_madera} - {self.clase_diametrica}'

