from django.db import models

class ProductosEmpresa(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, db_column='rut_empresa')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)

    class Meta:
        db_table = 'PRODUCTOS_EMPRESA'
