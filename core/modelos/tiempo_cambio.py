from django.db import models


class TiempoCambio(models.Model):
    valor = models.FloatField()
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')

    class Meta:
        db_table = 'TIEMPO_CAMBIO'
        
    def __str__(self):
        return f'valor de tiempo cambio = {self.valor}'