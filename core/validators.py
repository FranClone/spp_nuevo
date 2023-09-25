from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

def validate_rut(rut):
    #el guión no necesita validación
    if rut:
        rut = rut.replace("-", "")
        #el rut sólo puede ser digito y dígito + kK en caso del último dígito
        if not rut.isdigit() and rut[-1].upper() != 'K':
            raise ValidationError('El RUT solo puede contener números y un guión')
        if len(rut) < 8:
            raise ValidationError('El RUT es demasiado corto')
        #aquí empieza el algoritmo módulo 11
        dv_calculado = None
        factor = 2
        suma = 0
        for d in reversed(rut[:-1]):
            suma += int(d) * factor
            factor += 1
            if factor == 8:
                factor = 2
        resto = suma % 11
        if resto == 0:
            dv_calculado = '0'
        elif resto == 1:
            dv_calculado = 'K'
        else:
            dv_calculado = str(11 - resto)
        if dv_calculado != rut[-1].upper():
            raise ValidationError('El dígito verificador es incorrecto')
    
###
def validate_not_past_date(value):
    if value < date.today():
        raise ValidationError(
            _('Date cannot be in the past.'),
            code='date_in_past'
        )
