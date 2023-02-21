from django.db import models

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    rut_empresa = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    nombre_producto = models.CharField(max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    descripcion_producto = models.CharField(max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    espesor_producto = models.FloatField(blank=True, null=True)
    ancho_producto = models.FloatField(blank=True, null=True)
    largo_producto = models.FloatField(blank=True, null=True)
    usuario_crea = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fecha_crea = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'PRODUCTO'