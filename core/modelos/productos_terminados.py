from django.db import models

class ProductoTerminado(models.Model):
    codigo = models.CharField(max_length=20, null=False, blank=False)
    nombre = models.CharField(max_length=20, null=False, blank=False)
    grosor = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    ancho = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    largo = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    clase_diametrica = models.CharField(max_length=20, null=False, blank=False)
    patron_corte = models.CharField(max_length=50, null=False, blank=False)
    cantidad_producida = models.PositiveIntegerField(null=False, blank=False)
    fecha_produccion = models.DateField(null=True, blank=False)
    def __str__(self):
        return self.nombre
