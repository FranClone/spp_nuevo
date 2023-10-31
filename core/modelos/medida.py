from django.db import models
from .patron_corte import PatronCorte
from django.core.validators import MinValueValidator   
class Medida(models.Model):
    """Este modelo define la entidad Medido"""
    # Entradas
    alto_producto = models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    ancho_producto = models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    largo_producto = models.FloatField(validators=[MinValueValidator(0)], null=True)                                                   
    eliminado = models.BooleanField(default=False)
    
    def eliminar(self):
        # Marcar el registro como eliminado
        self.eliminado = True
        self.save()
        
    def __str__(self):
        return f'medidas {str(self.alto_producto)}-{str(self.ancho_producto)}-{str(self.largo_producto)}%'



