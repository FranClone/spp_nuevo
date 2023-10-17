from django.db import models
from django.core.validators import MinValueValidator   

class Linea(models.Model):
    #Velocidad de la linea, depende de la clase diametrica V
    patron = models.ForeignKey('PatronCorte', on_delete=models.CASCADE, verbose_name='Patrón de Corte')
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, verbose_name='Empresa', db_column='rut_empresa')
    nombre_linea = models.CharField(max_length=200, verbose_name = 'Linea')
    descripcion_linea = models.CharField(max_length=300, blank=True, null=True)
    velocidad = models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True) #m3/hr V
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    eliminado = models.BooleanField(default=False)
    
    def eliminar(self):
        # Marcar el registro como eliminado
        self.eliminado = True
        self.save()

    class Meta:
        db_table = 'LINEA'
        
    def __str__(self):
        return self.nombre_linea
