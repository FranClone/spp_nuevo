# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinValueValidator                                             
    
class DetallePedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, verbose_name='Pedido')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE, verbose_name='Producto')
    factura = models.ForeignKey('Factura', on_delete=models.CASCADE, verbose_name='Factura')
    empaque = models.ForeignKey('Empaque', on_delete=models.CASCADE, verbose_name='Empaque')
    producto_key = models.CharField(max_length=300, null=True)
    item = models.CharField(max_length=20, null=True, blank=False)
    folio =  models.CharField(max_length=20, null=True, blank=False)
    detalle_producto = models.CharField(max_length=300,null=True)
    alto_producto = models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    ancho_producto = models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    largo_producto = models.FloatField(validators=[MinValueValidator(0)], null=True)
    volumen_producto = models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    fecha_entrega = models.DateField(null=True)
    estado_pedido_linea = models.CharField(max_length=40, null=True, blank=False)
    #estado_pedido_linea = models.BooleanField(blank=True, null=True)
    grado_urgencia = models.CharField(max_length=100, null=True, blank=False)
    #piezas x paquete * paquetes saldo
    cantidad_piezas =  models.IntegerField(validators=[MinValueValidator(0)], null=True)
     #piezas * piezas x trozo
    cantidad_trozos =   models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    piezas_xpaquete =   models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    piezas_xtrozo =  models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    paquetes_solicitados =  models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    volumen_obtenido =  models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    paquetes_saldo = models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    mercado = models.CharField(max_length=40, null=True, blank=False)
    puerto_destino = models.CharField(max_length=40, null=True, blank=False)
    #detalles extra de la orden de pedido pdf
    term = models.CharField(max_length=40, null=True, blank=False)
    calidad = models.CharField(max_length=40, null=True, blank=False)
    mbf = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    banio = models.CharField(max_length=40, null=True, blank=False)
    marca = models.CharField(max_length=40, null=True, blank=False)
    programa = models.CharField(max_length=40, null=True, blank=False)
    piezas = models.FloatField(validators=[MinValueValidator(0)], null=True)
    cpo = models.FloatField(validators=[MinValueValidator(0)], null=True)
    piezas_x_cpo = models.FloatField(validators=[MinValueValidator(0)], null=True)
    est = models.CharField(max_length=40, null=True, blank=False) 
    separador = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    nota =models.CharField(max_length=200, null=True) 
    diametro = models.FloatField(max_length=10, validators=[MinValueValidator(0)],null=True)
    largo_trozo = models.DecimalField(max_digits=10,validators=[MinValueValidator(0)], decimal_places=3, null=True)
    
    def save(self, *args, **kwargs):
        # Calcula la concatenación de atributos
        self.producto_key = f"{self.producto}-{self.largo_producto}-{self.alto_producto}-{self.ancho_producto}"
        super().save(*args, **kwargs)
    class Meta:
        db_table = 'DETALLE_PEDIDO'
        
    def __str__(self):
        return self.detalle_producto
