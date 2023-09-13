from django.db import models


class Rollizo(models.Model):
    numero_buzon = models.IntegerField()
    nombre_rollizo = models.CharField(max_length=20, null=False, blank=False)
    descripcion_rollizo = models.CharField(max_length=500, blank=True, null=True)
    tipo_madera = models.CharField(max_length=10)
    clase_diametrica = models.CharField(max_length=10)
    largo = models.FloatField(max_length=10)
    diametro = models.IntegerField()
    cantidad = models.PositiveIntegerField(null=False, blank=False)
    conicidad = models.FloatField(max_length=10)
    linea_produccion = models.CharField(max_length=10)
    costo_almacenamiento = models.FloatField(max_length=10) # obviar por el momento
    inventario_buzon= models.PositiveIntegerField(null=False, blank=False)
    volumen_inicial = models.PositiveIntegerField(null=False, blank=False)
    costo_procesamiento = models.PositiveIntegerField(null=False, blank=False)
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    nombre=models.ForeignKey('MateriaPrima', on_delete=models.CASCADE)
    CLASE_DIAMETRICA_CHOICES = []
    for i in range(12, 31, 2):
        CLASE_DIAMETRICA_CHOICES.append((i, i))
    clase_diametrica = models.IntegerField(blank=True, null=True, choices=CLASE_DIAMETRICA_CHOICES)
  
    # Salidas
    volumen_procesado = models.FloatField(max_length=10)
    inventario_final = models.FloatField(max_length=10)
        
    def __str__(self):
        return f'Buzón {self.numero_buzon}: {self.cantidad} m3'