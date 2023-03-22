from django.db import models

class PatronCorte(models.Model):
    nombre_patron = models.CharField(max_length=300)
    descripcion_patron = models.CharField(max_length=500, blank=True, null=True)
    usuario_crea = models.CharField(max_length=30, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'PATRON_CORTE'

    def __str__(self):
        return self.nombre_patron
