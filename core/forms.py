from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import UserProfile

class BaseForm(forms.Form):
    def clean_rut(self, is_empresa=False):
        cleaned_data = super().clean()
        rut_body = cleaned_data.get("rut_body")
        rut_dv = cleaned_data.get("rut_dv")
        if is_empresa:
            rut_body = cleaned_data.get("rut_empresa_body")
            rut_dv = cleaned_data.get("rut_empresa_dv")
        rut = f"{rut_body}-{rut_dv}"

        if rut_body and rut_dv:
            def validate_rut(rut):
                rut = str(rut)
                rut = rut.replace("-", "")
                if not rut.isdigit() and rut[-1].upper() != 'K':
                    raise ValidationError('El RUT solo puede contener números y un guión')
                if len(rut) < 8:
                    raise ValidationError('El RUT es demasiado corto')
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
                else:
                    dv_calculado = str(11 - resto)
                if dv_calculado != rut[-1].upper():
                    raise ValidationError('El dígito verificador es incorrecto')


            try:
                validate_rut(rut)
            except ValidationError as e:
                raise forms.ValidationError(e)

            cleaned_data["rut" if not is_empresa else "rut_empresa"] = rut

        return cleaned_data


class CustomUserCreationForm(BaseForm, UserCreationForm):
    rut_body = forms.CharField(
        widget=forms.TextInput(attrs={'inputmode': 'numeric', 'class' : 'rut-body'}),
        label="RUT",
        max_length=8
    )   
    rut_dv = forms.CharField(
        max_length=1, 
        label="digito rutificador",
        widget=forms.TextInput(attrs={'class': 'rut-dv'})
    )
    rut_empresa_body = forms.CharField(
        widget=forms.TextInput(attrs={'inputmode' : 'numeric', 'class' : 'rut-body rut-body-empresa'}),
        label="RUT empresa",
        max_length=8
    )
    rut_empresa_dv = forms.CharField(
        max_length=1, 
        label="digito rutificador empresa", 
        widget=forms.TextInput(attrs={'class': 'rut-dv'})
    )
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="grupo")
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'rut_body', 'rut_dv', 'rut_empresa_body', 'rut_empresa_dv', 'group']

    def clean(self):
        cleaned_data = super().clean()
        self.clean_rut()                # Validate the regular RUT
        self.clean_rut(is_empresa=True) # Validate the empresa RUT
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rut = self.cleaned_data['rut']
        user.rut_empresa = self.cleaned_data['rut_empresa']
        if commit:
            try:
                # Validar si ya existe un UserProfile con el mismo RUT
                if UserProfile.objects.filter(rut=user.rut).exists():
                    raise IntegrityError('El RUT ya se encuentra registrado en el sistema.')
                user.save()
            except IntegrityError:
                raise forms.ValidationError('El RUT ya se encuentra registrado en el sistema.')
        group = self.cleaned_data['group']
        user.groups.add(group)
        return user

class LoginForm(BaseForm):
    rut_body = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login rut-body', 'placeholder': 'RUT Cliente'}), max_length=8, label="")
    rut_dv = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login rut-dv'}), max_length=1, label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-login', 'placeholder': 'Contraseña'}), max_length=60, label="")

    def clean(self):
        cleaned_data = super().clean()
        self.clean_rut()
        return cleaned_data