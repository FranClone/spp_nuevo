from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
#from .models import UserProfile
from .modelos.empresa import Empresa

#probar esto

class CustomUserCreationForm(UserCreationForm):
    #campo rut_body
    rut_body = forms.CharField(
        widget=forms.TextInput(attrs={'inputmode': 'numeric', 'class' : 'input-rut-body'}),
        label="RUT",
        max_length=8
    )
    #campo rut_dv
    rut_dv = forms.CharField(
        max_length=1, 
        label="digito rutificador",
        widget=forms.TextInput(attrs={'class': 'input-rut-dv'})
    )
    #campo rut_empresa_body
    rut_empresa_body = forms.CharField(
        widget=forms.TextInput(attrs={'inputmode' : 'numeric', 'class' : 'input-rut-body rut-body-empresa'}),
        label="RUT empresa",
        max_length=8
    )
    #campo rut_empresa_dv
    rut_empresa_dv = forms.CharField(
        max_length=1, 
        label="digito rutificador empresa", 
        widget=forms.TextInput(attrs={'class': 'input-rut-dv'})
    )

    #grupos creados
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="grupo")

    #class Meta especifica detalles importantes del formulario, en este caso el modelo y los campos
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'rut_body', 'rut_dv', 'rut_empresa_body', 'rut_empresa_dv', 'group']

    def clean(self):
        #se hace la validación del modelo
        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rut = self.cleaned_data['rut']
        user.rut_empresa = self.cleaned_data['rut_empresa']
        if commit:
            try:
                # Validar si ya existe un UserProfile con el mismo RUT
                #if UserProfile.objects.filter(rut=user.rut).exists():
                    #raise IntegrityError('El RUT ya se encuentra registrado en el sistema.')
                user.save()
            except IntegrityError:
                raise forms.ValidationError('El RUT ya se encuentra registrado en el sistema.')
        group = self.cleaned_data['group']
        user.groups.add(group)
        return user

class LoginForm(forms.Form):
    rut_body = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-rut-body', 'placeholder': '12345678'}), max_length=8, label="")
    rut_dv = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-rut-dv', 'placeholder': '9'}), max_length=1, label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}), max_length=25, label="")

    def clean(self):
        return super().clean()

#administracion limitacion de caracteres en procesos
user_name = forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'form-control-sm'}),
        label="Usuario",
        max_length=20
    )

correo = forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'form-control-sm'}),
        label="correo",
        max_length=25
    )
