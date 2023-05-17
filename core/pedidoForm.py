from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet, BaseModelFormSet, inlineformset_factory
from django.forms.widgets import DateInput
from django.core.validators import MinValueValidator
from datetime import datetime
from .modelos.pedido import Pedido
from .modelos.detalle_pedido import DetallePedido
from .modelos.cliente import Cliente
from .modelos.producto import Producto

import re

class PedidoForm(forms.ModelForm):
    fecha_recepcion = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    fecha_entrega = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Pedido
        fields = ['numero_pedido', 'destino_pedido', 'fecha_recepcion', 'fecha_entrega', 'cliente', 'prioridad', 'estado_pedido']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['cliente'].queryset = Cliente.objects.filter(empresa=user.empresa)

class DetallePedidoForm(forms.ModelForm):
    fecha_entrega = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    espesor_producto = forms.DecimalField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'style': 'width: 100px;'})
    )
    largo_producto = forms.DecimalField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'style': 'width: 100px;'})
    )
    volumen_producto = forms.DecimalField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'style': 'width: 100px;'})
    )
    class Meta:
        model = DetallePedido
        fields = ['producto', 'detalle_producto', 'espesor_producto', 'ancho_producto', 'largo_producto', 'volumen_producto', 'fecha_entrega', 'estado_pedido_linea']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['producto'].queryset = Producto.objects.filter(empresa=user.empresa)

class DetallePedidoFormSetBase(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.user = user

    def _construct_form(self, i, **kwargs):
        kwargs['user'] = self.user
        return super()._construct_form(i, **kwargs)

DetallePedidoFormSet = formset_factory(
    DetallePedidoForm,
    formset = DetallePedidoFormSetBase,
    extra=1,
    can_delete=True,
)
