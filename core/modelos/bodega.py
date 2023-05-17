from django.db import models

class Bodega(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, verbose_name='Empresa', db_column='rut_empresa')
    nombre_bodega = models.CharField(max_length=200, verbose_name = 'Bodega')
    descripcion_bodega = models.CharField(max_length=300, blank=True, null=True)
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True, null=True)
    ubicacion = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'BODEGA'

    def __str__(self):
        return self.nombre_bodega