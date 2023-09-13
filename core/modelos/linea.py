from django.db import models


class Linea(models.Model):
    nombre_linea = models.CharField(max_length=200, verbose_name = 'Linea')
    descripcion_linea = models.CharField(max_length=300, blank=True, null=True)
    capacidad_maxima= models.PositiveIntegerField(null=False, blank=False)
    velocidad_linea= models.PositiveIntegerField(null=False, blank=False)
    capacidad_disponible= models.PositiveIntegerField(null=False, blank=False)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, verbose_name='Empresa', db_column='rut_empresa')
    rollizo = models.ForeignKey('Rollizo', on_delete=models.CASCADE) 
    nombre = models.ForeignKey('PatronCorte', on_delete=models.CASCADE) 
    nombre = models.ForeignKey('MateriaPrima', on_delete=models.CASCADE) 
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'LINEA'
        
    def __str__(self):
        return self.nombre_linea
