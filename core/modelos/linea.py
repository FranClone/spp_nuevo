from django.db import models


class Linea(models.Model):
    nombre_linea = models.CharField(max_length=200, verbose_name = 'Linea')
    descripcion_linea = models.CharField(max_length=300, blank=True, null=True)
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'LINEA'
        
    def __str__(self):
        return self.nombre_linea
