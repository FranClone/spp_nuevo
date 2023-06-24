from django.db import models

class Pedido(models.Model):
    cliente = models.CharField(max_length=50, null=False, blank=False)
    fecha_entrega = models.DateField(null=False, blank=False)
    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=20, null=False, blank=False)
    grosor = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    ancho = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    largo = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    productos_a_producir = models.TextField(null=False, blank=False)
    cantidad = models.PositiveIntegerField(null=False, blank=False)
    numero_pedido = models.CharField(max_length=20, null=False, blank=False)
    estado_pedido = models.CharField(max_length=20, null=False, blank=False)
    prioridad = models.IntegerField(null=False, blank=False)
    destino_pedido = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"Pedido {self.codigo} - Cliente: {self.cliente}"
