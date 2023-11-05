from django.db import models

#ver que hacer con id_periodo, de momento está borrado pero se modificó
from django.core.validators import MinValueValidator   
class LineaHhDisponible(models.Model):
    #Capacidad teorica disponible de la linea(delgada o gruesa) medida en horas x periodo (turno) CAPD
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, verbose_name='Empresa', db_column='rut_empresa')
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    periodo = models.ForeignKey('Periodo', on_delete=models.CASCADE, verbose_name='Periodo')
    numero_bloque = models.IntegerField(null=False,validators=[MinValueValidator(0)])
    cantidad_hh = models.IntegerField(null=False,validators=[MinValueValidator(0)])
    dias_produccion = models.DateField(null=False)
    usuario_crea = models.CharField(max_length=20, blank=True, null=False)
    fecha_crea = models.DateField(auto_now_add=True)


    class Meta:
        db_table = 'LINEA_HH_DISPONIBLE'

    def __str__(self):
        return 'id de Linea Horas Hombre Disponible: ' + str(self.id)