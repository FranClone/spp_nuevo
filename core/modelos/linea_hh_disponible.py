from django.db import models

#ver que hacer con id_periodo, de momento está borrado pero se modificó

class LineaHhDisponible(models.Model):
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    numero_bloque = models.IntegerField()
    cantidad_hh = models.IntegerField()
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, verbose_name='Empresa', db_column='rut_empresa')

    class Meta:
        db_table = 'LINEA_HH_DISPONIBLE'

    def __str__(self):
        return 'id de Linea Horas Hombre Disponible: ' + str(self.id_hh_linea)