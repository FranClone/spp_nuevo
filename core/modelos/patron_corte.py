from django.db import models

class PatronCorte(models.Model):
    """Este modelo define la entidad Patrón de Corte"""
    
    # Entradas 
    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False, default='')
    nombre = models.CharField(max_length=20, null=False, blank=False)
    descripcion = models.CharField(max_length=20, null=False, blank=False)
    rollizo = models.CharField(max_length=10)
    rendimiento = models.FloatField(max_length=5)
    velocidad_linea = models.FloatField(max_length=5)
    setup_time = models.FloatField(max_length=5)
    lead_time = models.FloatField(max_length=5)

    # Salidas
    utilizado = models.BooleanField()
    producto_asociado = models.CharField(max_length=20, null=False, blank=False, default='')

    def __str__(self):
        return f'Patrón de corte {self.codigo}: {self.rendimiento} %'
