from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class BaseForm(forms.Form):
    def clean_rut(self):
        cleaned_data = super().clean()
        rut_body = cleaned_data.get("rut_body")
        rut_dv = cleaned_data.get("rut_dv")
        rut = f"{rut_body}-{rut_dv}"

        if rut_body and rut_dv:
            def validate_rut(rut):
                rut = str(rut)
                rut = rut.replace("-", "")
                if not rut.isdigit() and rut[-1].upper() != 'K':
                    raise ValidationError('El RUT solo puede contener números y un guión')
                if len(rut) < 8:
                    raise ValidationError('El RUT es demasiado corto')

                v = 11 - sum(int(x) * (i + 2) for i, x in enumerate(reversed(rut[:-1]))) % 11
                if v == 10:
                    digit = 'K'
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


class CustomUserCreationForm(BaseForm, UserCreationForm):
    rut_body = forms.CharField(max_length=8, label="")
    rut_dv = forms.CharField(max_length=1, label="")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'rut_body', 'rut_dv']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rut = self.cleaned_data['rut']
        if commit:
            user.save()
        return user

class LoginForm(BaseForm):
    rut_body = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login rut-body', 'placeholder': 'RUT Cliente'}), max_length=8, label="")
    rut_dv = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login rut-dv'}), max_length=1, label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-login', 'placeholder': 'Contraseña'}), max_length=60, label="")
