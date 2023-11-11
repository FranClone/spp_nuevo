from django.db import models

class AbastecimientoRollizo(models.Model):
    rollizo = models.ForeignKey('Rollizo', on_delete=models.CASCADE, verbose_name='Rollizo')
    periodo = models.ForeignKey('Periodo', on_delete=models.CASCADE, verbose_name='Periodo')
    numero_bloque = models.IntegerField(blank=True, null=True)
    cantidad_hh = models.IntegerField(blank=True, null=True)
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'ABASTECIMIENTO_ROLLIZO'
        ordering = ['id']
        
    def __str__(self):
        return f'Abastecimiento de rollizo = {self.numero_bloque} y cantidad = {self.cantidad_hh}'
 # Hola