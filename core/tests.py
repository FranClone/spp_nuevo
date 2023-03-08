from django.test import TestCase
from django.core.exceptions import ValidationError
from .modelos.empresa import Empresa

class EmpresaTestCase(TestCase):
    def test_rut_validation(self):
        # Crear una empresa con un rut válido
        empresa_valida = Empresa(rut_empresa='90100729-2', nombre_empresa='Empresa 1')
        try:
            empresa_valida.full_clean()
        except ValidationError as e:
            self.fail('La validación del rut no debería haber fallado con un rut válido')

        # Crear una empresa con un rut inválido
        empresa_invalida = Empresa(rut_empresa='90100729-3', nombre_empresa='Empresa 2')
        with self.assertRaises(ValidationError):
            empresa_invalida.full_clean()