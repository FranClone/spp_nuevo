from django.db import models

class ClienteEmpresa(models.Model):
    empresa_oferente = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='oferente')
    empresa_cliente = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='cliente')

    class Meta:
        db_table = 'CLIENTE_EMPRESA'
        constraints = [
            models.UniqueConstraint(fields=['empresa_oferente', 'empresa_cliente'], name='unique_relacion_empresa')
        ]