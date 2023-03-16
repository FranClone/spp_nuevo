from django import forms
from django.forms import formset_factory
from datetime import datetime
from .modelos.producto import Producto
import pyodbc, os, re

class ProductoForm(forms.Form):
    #Se obtienen los productos desde un desplegable
    producto = forms.ChoiceField()
    #La cantidad se ingresa desde un input integer
    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'min':'1'}))
    def __init__(self, *args, rut_empresa=None, **kwargs):
        self.rut_empresa = rut_empresa
        super().__init__(*args, **kwargs)
        data_productos = Producto.objects.filter(productosempresa__rut_empresa__rut_empresa=rut_empresa)
        choices = [(producto.nombre_producto, producto.nombre_producto) for producto in data_productos]
        self.fields['producto'] = forms.ChoiceField(choices=choices)

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        if cantidad < 1:
            self.add_error("cantidad", "La cantidad no puede ser negativa o 0")

ProductoFormSet = formset_factory(ProductoForm, extra=1)

class PedidoForm(forms.Form):
    numero_pedido = forms.IntegerField(widget=forms.NumberInput(attrs={'min':'1'}), label="Número Pedido")
    fecha_recepcion = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    fecha_entrega = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    destino_pedido = forms.CharField(max_length=100)
    prioridad = forms.ChoiceField(choices=(('Alta','Alta'), ('Media', 'Media'), ('Baja', 'Baja'), ('Eliminada', 'Eliminada')))
    def __init__(self, rut_empresa, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rut_empresa = rut_empresa
        self.productos = ProductoFormSet(form_kwargs={'rut_empresa': self.rut_empresa})
        """conexion = pyodbc.connect(os.environ.get('CONEXION_BD'))
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_bodega_empresa @rut_empresa=?", os.environ.get('RUT_EMPRESA'))
        data_bodegas = cursor.fetchall()
        choices = [(bodega.id_bodega, bodega.nombre_bodega) for bodega in data_bodegas]
        self.fields['nombre_bodega'] = forms.ChoiceField(choices=choices)"""
    

    def clean(self):
        cleaned_data = super().clean()
        numero_pedido = cleaned_data.get("numero_pedido")
        fecha_recepcion = cleaned_data.get("fecha_recepcion")
        fecha_entrega = cleaned_data.get("fecha_entrega")
        destino_pedido = self.cleaned_data.get('destino_pedido')
        if not re.match(r'^[a-zA-ZÁÉÍÓÚÑáéíóúñ ]+$', destino_pedido):
            self.add_error("destino_pedido", "El destino ingresado no es una ciudad válida.")

        if fecha_recepcion and fecha_entrega and numero_pedido:
            if fecha_recepcion > fecha_entrega:
                self.add_error("fecha_recepcion", "La fecha de recepción no puede ser mayor a la fecha de entrega")
            if fecha_recepcion < datetime.today().date():
                self.add_error("fecha_recepcion", "La fecha de recepción no puede ser menor al día de hoy")
            if fecha_entrega < datetime.today().date():
                self.add_error("fecha_entrega", "La fecha de entrega no puede ser menor al día de hoy")
            if numero_pedido < 0:
                self.add_error("numero_pedido", "El número de pedido no puede ser negativo")