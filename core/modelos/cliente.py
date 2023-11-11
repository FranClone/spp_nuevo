from django.db import models
from django.core.exceptions import ValidationError
from ..validators import validate_rut

class Cliente(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, db_column='rut_empresa')
    rut_cliente = models.CharField(max_length=20)
    nombre_cliente = models.CharField(max_length=100, verbose_name='Cliente')
    correo_cliente = models.CharField(max_length=300, blank=True, null=False)
#    estado_cliente = models.BooleanField(blank=True, null=True)
#    fecha_vigencia = models.DateField(blank=True, null=True)
    fecha_crea = models.DateField(auto_now_add=True)
    usuario_crea = models.CharField(max_length=20, blank=True, null=False)
#    nombre_fantasia = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=False)
    telefono = models.IntegerField(blank=True, null=False)
    mercado = models.CharField(max_length=100)
    puerto_destino  = models.CharField(max_length=100)
    eliminado = models.BooleanField(default=False)
    
    def eliminar(self):
        # Marcar el registro como eliminado
        self.eliminado = True
        self.save()
    class Meta:
        db_table = 'CLIENTE'

    def __str__(self):
        return self.nombre_cliente
    
    def clean(self):
        super().clean()
        try:
            validate_rut(self.rut_cliente)
        except ValidationError as e:
            raise ValidationError({'rut_cliente': e})