from django.db import models
class ClienteEmpresa(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    # otros campos adicionales aquí

    class Meta:
        db_table = 'CLIENTE_EMPRESA'

    def __str__(self):
        return f'{self.cliente} trabaja en {self.empresa}'