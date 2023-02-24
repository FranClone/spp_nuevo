from django.db import models

class Empresa(models.Model):
    rut_empresa = models.CharField(primary_key=True, max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    nombre_empresa = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    correo_empresa = models.CharField(max_length=300, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    estado_empresa = models.BooleanField(blank=True, null=True)
    id_periodo = models.IntegerField(blank=True, null=True)
    fecha_vigencia = models.DateField(blank=True, null=True)
    fecha_crea = models.DateField(blank=True, null=True)
    usuario_crea = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    nombre_fantasia = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ciudad = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'EMPRESA'


    def __str__(self):
        return self.nombre_empresa