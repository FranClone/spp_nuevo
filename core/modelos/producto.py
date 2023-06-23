from django.db import models

class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=20, null=False, blank=False)
    grosor = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    ancho = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    largo = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.nombre

