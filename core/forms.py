from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    rut = forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'rut']

class LoginForm(forms.Form):
    rut = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-login', 'placeholder': 'RUT Cliente','style': 'margin-bottom:8px;'}), max_length=20, label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-login', 'placeholder': 'Contraseña','style': 'margin-bottom:8px;'}), max_length=60, label="")