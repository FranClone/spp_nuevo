from django.db import models


class Pedido(models.Model):
    numero_pedido = models.CharField(max_length=200, verbose_name='Número de Pedido')
    destino_pedido = models.CharField(max_length=300)
    fecha_recepcion = models.DateField()
    fecha_entrega = models.DateField()
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    estado_pedido = models.BooleanField()
    PRIORIDAD_CHOICES = [
        ('Alta', 'Alta'),
        ('Media', 'Media'),
        ('Baja', 'Baja'),
    ]
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES)
    productos = models.ManyToManyField('Producto', through='detallepedido')

    class Meta:
        db_table = 'PEDIDO'

    def __str__(self):
        return 'Número de Pedido: ' + self.numero_pedido