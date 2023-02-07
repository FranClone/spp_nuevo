from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def validate_rut_body(value):
    if not value.isdigit():
        raise forms.ValidationError('El RUT debe ser un número.')
    return value

def validate_rut_dv(value):
    if not (value.isdigit() or value.lower() == 'k'):
        raise forms.ValidationError('El DV debe ser un número o una K.')
    return value

class CustomUserCreationForm(UserCreationForm):
    rut_body = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login rut-body', 'placeholder': 'RUT Cliente', 'input_type': 'number'}), max_length=8, label="", validators=[validate_rut_body])
    rut_dv = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login rut-dv'}), max_length=1, label="", validators=[validate_rut_dv])

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'rut_body', 'rut_dv']

    def clean(self):
        cleaned_data = super().clean()
        rut_body = cleaned_data.get("rut_body")
        rut_dv = cleaned_data.get("rut_dv")
        if not rut_body or not rut_dv:
            raise forms.ValidationError("Debe ingresar un RUT válido")
        cleaned_data["rut"] = rut_body + "-" + rut_dv
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rut = self.cleaned_data['rut']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    rut_body = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login rut-body', 'placeholder': 'RUT Cliente'}), validators=[validate_rut_body], max_length=8, label="")
    rut_dv = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login rut-dv'}), validators=[validate_rut_body], max_length=1, label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-login', 'placeholder': 'Contraseña'}), max_length=60, label="")
    def clean_rut(self):
        cleaned_data = super().clean()
        rut_body = cleaned_data.get("rut_body")
        rut_dv = cleaned_data.get("rut_dv")
        if rut_body and rut_dv:
            rut = f"{rut_body}-{rut_dv}"

            def validate_rut(rut):
                rut = str(rut)
                rut = rut.replace("-", "")
                if not rut.isdigit():
                    raise ValidationError('El RUT solo puede contener números y un guión')
                if len(rut) < 8:
                    raise ValidationError('El RUT es demasiado corto')

                v = 11 - sum(int(x) * (i + 2) for i, x in enumerate(reversed(rut[:-1]))) % 11
                if v == 10:
                    digit = 'k'
                elif v == 11:
                    digit = '0'
                else:
                    digit = str(v)

                if digit.lower() != rut[-1].lower():
                    raise ValidationError('El dígito verificador es incorrecto')

            try:
                validate_rut(rut)
            except ValidationError as e:
                raise forms.ValidationError(e)

            cleaned_data["rut"] = rut

        return cleaned_data
