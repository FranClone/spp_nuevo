from django.db import models


class TipoPeriodo(models.Model):
    nombre_tipo_periodo = models.CharField(max_length=200)
    descripcion_tipo_periodo = models.CharField(max_length=500, blank=True, null=True)
    dias = models.IntegerField(blank=True, null=True)
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    empresa = models.OneToOneField('Empresa', on_delete=models.CASCADE, verbose_name='Empresa', db_column='rut_empresa')

    class Meta:
        db_table = 'TIPO_PERIODO'

    def __str__(self):
        return self.nombre_tipo_periodo