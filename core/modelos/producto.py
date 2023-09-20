from django.db import models
from .patron_corte import PatronCorte
class Producto(models.Model):
    """Este modelo define la entidad Producto"""
    
    # Entradas
    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=20, null=False, blank=False)
    descripcion = models.CharField(max_length=100, null=False, blank=False)
    largo = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    ancho = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)    
    alto = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    grado_urgencia = models.CharField(max_length=100, null=False, blank=False)
    inventario_inicial = models.FloatField(max_length=10)
    valor_inventario = models.FloatField(max_length=10)
    costo_almacenamiento = models.FloatField(max_length=10)
    paquetes_solicitados = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    paquetes_saldo = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    #piezas x paquete * paquetes saldo
    cantidad_piezas = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
     #piezas * piezas x trozo
    cantidad_trozos = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    piezas_xpaquete = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    piezas_xtrozo = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    #Foranea rollizo
    nombre_rollizo = models.ForeignKey('Rollizo', on_delete=models.CASCADE, verbose_name='Rollizo')
    # Salidas
    volumen_obtenido = models.FloatField(max_length=10)
    inventario_final = models.FloatField(max_length=10)
    patron_corte = models.ManyToManyField(PatronCorte)   
    #Linea de corte
    linea = models.ForeignKey('Linea', on_delete=models.CASCADE, verbose_name='Linea')
    def __str__(self):
        return f' {self.nombre}'

