from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet, BaseModelFormSet, inlineformset_factory
from django.forms.widgets import DateInput
from datetime import datetime
from .modelos.pedido import Pedido
from .modelos.detalle_pedido import DetallePedido
from .modelos.cliente import Cliente

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

    class Meta:
        model = DetallePedido
        fields = ['producto', 'detalle_producto', 'volumen_producto', 'fecha_entrega', 'estado_pedido_linea']
        

DetallePedidoFormSet = formset_factory(
    DetallePedidoForm,
    extra=1,
    can_delete=True,
)
