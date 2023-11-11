from django.db import models
from .patron_corte import PatronCorte
from .producto import Producto

class Rendimiento_Producto(models.Model):
    patron_id = models.ForeignKey(PatronCorte, on_delete=models.CASCADE)
    producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    rendimiento = models.IntegerField(null=True, blank=True) 

    class Meta:
        db_table = 'Rendimiento_Producto'