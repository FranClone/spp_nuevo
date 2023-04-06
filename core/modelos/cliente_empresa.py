from django.db import models
from django.core.exceptions import ValidationError

class ClienteEmpresa(models.Model):
    empresa_oferente = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='oferente')
    empresa_cliente = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='cliente')
    fecha_crea = models.DateField(auto_now_add=True)
    usuario_crea = models.CharField(max_length=20, blank=True, null=True)
    estado_cliente = models.BooleanField(default=True)

    class Meta:
        db_table = 'CLIENTE_EMPRESA'
        constraints = [
            models.UniqueConstraint(fields=['empresa_oferente', 'empresa_cliente'], name='unique_relacion_empresa')
        ]

    def __str__(self):
        return self.empresa_cliente.nombre_empresa
    
    def clean(self):
        if self.empresa_oferente == self.empresa_cliente:
            raise ValidationError("La empresa oferente y la empresa cliente deben ser distintas.")