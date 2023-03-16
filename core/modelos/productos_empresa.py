from django.db import models

class ProductosEmpresa(models.Model):
    id_pempresa = models.AutoField(primary_key=True)
    rut_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, db_column='rut_empresa')
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE, db_column='id_producto')

    class Meta:
        db_table = 'PRODUCTOS_EMPRESA'
