from django.db import models

class Demanda(models.Model):
    Medida_Producto_id = models.PositiveIntegerField(null=True)
    dias_produccion = models.DateField(null=True)
    Pqtes_Solicitados = models.PositiveIntegerField(null=True)
    Pqtes_dia = models.PositiveIntegerField(null=True)
    M3 = models.FloatField(null=True)
    class Meta:
        db_table = 'Demanda'
        
    def __str__(self):
        return self.dias_produccion
