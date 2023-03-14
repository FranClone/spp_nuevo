from django.db import models

class ProductosEmpresa(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)