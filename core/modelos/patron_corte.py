from django.db import models

class PatronCorte(models.Model):
    codigo_patron = models.CharField(max_length=20, unique=True, null=False, blank=False, default='Valor predeterminado')
    nombre_patron = models.CharField(max_length=20, null=False, blank=False)
    producto_asociado = models.CharField(max_length=20, null=False, blank=False, default='Valor predeterminado')
    clase_diametrica_rollizo = models.CharField(max_length=20, null=False, blank=False, default='Valor predeterminado')

    def __str__(self):
        return self.nombre_patron
