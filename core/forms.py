from django import forms
from django.contrib.auth.forms import UserCreationForm
from asignaciones.models import UserProfile
from .modelos.empresa import Empresa
from .modelos.materia_prima import MateriaPrima
from .modelos.patron_corte import PatronCorte
from .modelos.pedidos import Pedido
from .modelos.producto import Producto
from .modelos.rollizo import Rollizo
from .modelos.linea import Linea
from .modelos.cliente import Cliente
from .modelos.factura import Factura
from .modelos.empaque import Empaque
from .modelos.stock_producto import StockProducto
from .modelos.medida import Medida
from .modelos.producto_medida import ProductoMedida
from .modelos.productos_terminados import ProductoTerminado
from .modelos.stock_rollizo import StockRollizo
from .modelos.detalle_pedido import DetallePedido
from .modelos.bodega import Bodega
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.core.validators import MinValueValidator     
class Excelform(forms.Form):
    excel_file = forms.FileField()

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


    #class Meta especifica detalles importantes del formulario, en este caso el modelo y los campos
    class Meta:
        model = UserProfile
        fields = ['username', 'password1', 'password2', 'rut_body', 'rut_dv', 'rut_empresa_body', 'rut_empresa_dv']

    def clean(self):
        #se hace la validación del modelo
        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        rut_body = self.cleaned_data['rut_body']
        rut_dv = self.cleaned_data['rut_dv']
        rut_body_e = self.cleaned_data['rut_empresa_body']
        rut_dv_e = self.cleaned_data['rut_empresa_dv']
        rut_empresa = f'{rut_body_e}-{rut_dv_e}'
        user.rut = f'{rut_body}-{rut_dv}'
        empresa = Empresa.objects.filter(rut_empresa=rut_empresa).first()
        if empresa:
            user.empresa = empresa
        else:
            raise ValueError('No se encontró una instancia válida de Empresa')
        return user

class LoginForm(forms.Form):
    rut_body = forms.CharField(max_length=8, label="")
    rut_dv = forms.CharField(max_length=1, label="")
    password = forms.CharField(max_length=25, label="")

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

class ActualizarMateriaPrimaForm(forms.ModelForm):
    """Esta clase permite actualizar la materia prima de la vista de 'Materia Prima'"""
    numero_buzon =forms.FloatField(min_value=0)
    largo =forms.FloatField(min_value=0)
    cantidad =forms.FloatField(min_value=0)
    numero_buzon =forms.FloatField(min_value=0)
    inventario_inicial =forms.FloatField(min_value=0)
    volumen_procesado =forms.FloatField(min_value=0)
    inventario_final =forms.FloatField(min_value=0)
    class Meta:
        model = MateriaPrima
        fields = '__all__'

class CrearPatronCorteForm(forms.ModelForm):
    """Esta clase permite crear un nuevo patrón de corte"""
    ##Validaciones 
    rendimiento = forms.FloatField(min_value=0,max_value=2000)
    class Meta:
        model = PatronCorte
        fields = '__all__'

 
class CrearProductoForm(forms.ModelForm):
    """Esta clase permite crear un nuevo producto"""
    inventario_inicial = forms.FloatField(min_value=0)
    inventario_final = forms.FloatField(min_value=0)
    exclude = ['eliminado', 'empresa']
    class Meta:
        model = Producto
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['linea'].queryset = Linea.objects.filter(eliminado=False)
        self.fields['nombre_rollizo'].queryset = Rollizo.objects.filter(eliminado=False)
        self.fields['patron_corte'].queryset = PatronCorte.objects.filter(eliminado=False)


class CrearRollizoForm(forms.ModelForm):
    exclude = ['fecha_crea']
    class Meta:
        model = Rollizo
        fields ='__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CrearLineaForm(forms.ModelForm):
    exclude = ['fecha_crea']
    class Meta:
        model = Linea
        fields ='__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empresa'].queryset = Empresa.objects.filter(eliminado=False)
        
class CrearClienteForm(forms.ModelForm):
    exclude = ['fecha_crea']
    class Meta:
        model = Cliente
        fields ='__all__'
        
class CrearEmpresaForm(forms.ModelForm):
    fecha_vigencia = forms.DateField(
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'autocomplete': 'on',  # Desactiva el autocompletado del navegador
                'placeholder': 'dd/mm/yyyy',  # Formato de marcador de posición para la fecha
                'type': 'date',  # Utiliza el widget de fecha HTML5
            }
        )
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_vigencia'].widget.attrs.update({'class': 'form-control'})
    exclude = ['fecha_crea']
    class Meta:
        model = Empresa
        fields ='__all__'

 

class DetallePedidoForm(forms.ModelForm):
    pqte = forms.IntegerField(min_value=0)  # Adjust the field type and options as needed
    tipo_empaque = forms.CharField( max_length=50)
    alto_paquete =  forms.FloatField(min_value=0)
    int_paquete =  forms.FloatField(min_value=0)
    anc_paquete =  forms.FloatField(min_value=0)
    FSC = forms.CharField(max_length=100)
    esp_fact =  forms.FloatField( min_value=0)
    anc_fact =  forms.FloatField( min_value=0)
    lar_fact =  forms.FloatField( min_value=0)
    alto_producto =  forms.FloatField( min_value=0)
    ancho_producto =  forms.FloatField( min_value=0)
    largo_producto =  forms.FloatField( min_value=0)
    cpo =  forms.FloatField( min_value=0)
    piezas =  forms.FloatField( min_value=0)
    volumen_producto =  forms.DecimalField(max_digits=10,min_value=0, decimal_places=3)
    mbf =  forms.DecimalField(max_digits=10,min_value=0, decimal_places=3)
    id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = DetallePedido
        exclude = [
    
                    'fecha_salida',
                ]
        fields = '__all__'
     
    # producto = forms.ModelChoiceField(
    #     required=False,  # Hacerlo opcional
    #     queryset=Producto.objects.filter(eliminado=False),
    #     widget=forms.Select(choices=Producto.objects.values_list('id', 'nombre'))
    # )

    def save(self, commit=True):
        instance = super().save(commit=False)
        # //producto = self.cleaned_data.get('producto')
        # print(producto)
        # if producto:

        #     # Access the id of the related Producto
        #     producto_id = producto.id
        #     print(producto_id)
        #     instance.detalle_producto = producto.nombre  # Fill detalle_producto with product name
        # if instance.pedido:
        #     instance.pedido.producto.add(producto)

        if self.instance.pedido:  # Check if there's an associated Pedido
            instance.fecha_entrega = self.instance.pedido.fecha_entrega  
        cantidad_piezas = self.cleaned_data.get('piezas')
        if cantidad_piezas is not None:
            instance.cantidad_piezas = cantidad_piezas
        else:
            instance.cantidad_piezas = 0  # Or handle it based on your requirements

        # Calculate and set piezas_x_cpo
        cpo = self.cleaned_data.get('cpo')
        if cpo is not None:
            instance.piezas_x_cpo = instance.cantidad_piezas * cpo
        else:
            instance.piezas_x_cpo = 0  # Or handle it based on your requirements


        if commit:
            instance.save()        
        return instance

class ActualizarPedidoForm(forms.ModelForm):
    fecha_entrega = forms.DateField(
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'autocomplete': 'on',  # Desactiva el autocompletado del navegador
                'placeholder': 'dd/mm/yyyy',  # Formato de marcador de posición para la fecha
                'type': 'date',  # Utiliza el widget de fecha HTML5
            }
        )
    )
    fecha_produccion = forms.DateField(
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={
                'autocomplete': 'on',
                'placeholder': 'dd/mm/yyyy',
                'type': 'date',
            }
        )
    )
    # producto = forms.ModelChoiceField(
    #     required=False,
    #     queryset=Producto.objects.filter(eliminado=False),
    #     widget=forms.Select(choices=Producto.objects.values_list('id', 'nombre'))
    # )


        # self.fields['producto'].widget = forms.Select(choices=Producto.objects.values_list('id', 'nombre'))
        # self.fields['producto'].queryset = Producto.objects.filter(eliminado=False)

    class Meta:
         model = Pedido
         fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.filter(eliminado=False)
        self.fields['fecha_entrega'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_produccion'].widget.attrs.update({'class': 'form-control'})

DetallePedidoFormSet = inlineformset_factory(
    Pedido,  # Parent model
    DetallePedido,  # Child model
    form=DetallePedidoForm,  # Use the modified DetallePedidoForm
    extra=1,  # Number of empty forms to display
    can_delete=True,  # Allow formset to delete records
)


   
class EmpaqueForm(forms.ModelForm):
    class Meta:
        model = Empaque
        fields = '__all__'  # Esto incluirá todos los campos del modelo en el formulario

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'  # Esto incluirá todos los campos del modelo en el formulario

class ProductoTerminadoForm(forms.ModelForm):
    """Esta clase permite crear un nuevo producto terminado"""

    class Meta:
        model = ProductoTerminado
        fields = '__all__'

class StockForm(forms.ModelForm):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(),required=False)
    medidas = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = StockProducto
        exclude = ['fecha_crea','valor_inventario','costo_almacenamiento']
        fields = ['bodega','producto', "medidas",'cantidad_m3',  'usuario_crea']


    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        self.fields['medidas'].choices = self.get_medidas_choices()

    def get_medidas_choices(self):
        choices = []
        for producto in Producto.objects.all():
            producto_id = producto.id
            print('for producto',producto)
            for medida in producto.medida.all():
                print('for medida',medida)
                choice = (f'{producto.id}-{medida.id}', f'{producto.nombre} ({medida.alto_producto}x{medida.ancho_producto}x{medida.largo_producto})')
                choices.append(choice)
        return choices

    # producto_id = forms.ModelChoiceField(queryset=Producto.objects.all(), label="Producto ID")
    # producto_medidas = forms.CharField(label="Medidas del Producto", required=False, widget=forms.TextInput(attrs={'readonly': True}))

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields['producto_id'].widget = forms.Select(attrs={'class': 'form-control'})

    # def clean(self):
    #     cleaned_data = super().clean()
    #     return cleaned_data
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


    #     # Obtén las opciones desde DetallePedido y conviértelas en una lista de tuplas (id, producto_key)
    #     choices = DetallePedido.objects.values_list('id', 'producto_key')

    #     # Asigna las opciones al campo 'producto_key'
    #     self.fields['producto_key'].widget = forms.Select(choices=choices)
    #     self.fields['bodega'].widget = forms.Select(choices=Bodega.objects.values_list('id', 'nombre_bodega'))


      #  self.fields['bodega'].widget = forms.Select(choices=Bodega.objects.values_list('id', 'nombre_bodega'))

    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     detalle_pedido_id = cleaned_data.get('producto_key')  # Obtén el ID del DetallePedido seleccionado
    #     cantidad_a_agregar = cleaned_data.get('cantidad_m3')
    #     bodega = cleaned_data.get('bodega')
    #     print(detalle_pedido_id)
    #     print(bodega)
    #     if not bodega:
    #         raise forms.ValidationError("Debe seleccionar una bodega válida.")
        
    #     # Obtén el DetallePedido correspondiente
    #     detalle_pedido = DetallePedido.objects.get(id=detalle_pedido_id)
    #     producto_key = detalle_pedido.producto_key
    #     bodega_id = bodega.id
    #     print(detalle_pedido)
    #     print("producto key",producto_key)
    #     print("bodega",bodega)
    #     # Verifica si ya existe un registro en StockProducto con el mismo producto_key y el mismo id de bodega
    #     stock_existente = StockProducto.objects.filter(producto_key=producto_key, bodega_id=bodega_id).first()
        
    #     if stock_existente:
    #         # Si existe, suma la cantidad a agregar a la cantidad existente
    #         stock_existente.cantidad_m3 += cantidad_a_agregar
    #         stock_existente.save()
    #         cleaned_data['cantidad_m3'] = stock_existente.cantidad_m3
    #     else:
    #         # Si no existe, simplemente usa la cantidad a agregar
    #         cleaned_data['cantidad_m3'] = cantidad_a_agregar

    #         # Además, crea un nuevo registro en StockProducto en la bodega especificada
    #         StockProducto.objects.create(producto_key=producto_key, bodega=bodega, cantidad_m3=cantidad_a_agregar, detalle=detalle_pedido)

    #     return cleaned_data


# class StockForm(forms.ModelForm):
# exclude = ['fecha_crea']

# class Meta:
# model = StockProducto
# fields = '__all__'

# def __init__(self, *args, **kwargs):
# super().__init__(*args, **kwargs)

# # Obtén las opciones desde DetallePedido y conviértelas en una lista de tuplas (id, producto_key)
# productos_unicos = DetallePedido.objects.values('producto_key').distinct()
# choices = [(detalle['producto_key'], detalle['producto_key']) for detalle in productos_unicos]

# # Asigna las opciones al campo 'producto_key'
# self.fields['producto_key'].widget = forms.Select(choices=choices)
# self.fields['bodega'].widget = forms.Select(choices=Bodega.objects.values_list('id', 'nombre_bodega'))

# def clean(self):
# cleaned_data = super().clean()
# detalle_pedido_id = cleaned_data.get('producto_key')
# cantidad_a_agregar = cleaned_data.get('cantidad_m3')
# bodega = cleaned_data.get('bodega')

# if not bodega:
# raise forms.ValidationError("Debe seleccionar una bodega válida.")

# bodega_id = bodega.id  # Accede a la propiedad 'id' del objeto Bodega
# print(bodega_id)
# # Verifica si ya existe un registro en StockProducto con el mismo producto_key y el mismo id de bodega
# stock_existente = StockProducto.objects.filter(producto_key=detalle_pedido_id, bodega_id=bodega_id).first()

# if stock_existente:

#     # Si existe, suma la cantidad a agregar a la cantidad existente
# stock_existente.cantidad_m3 += cantidad_a_agregar
# cleaned_data['cantidad_m3'] = stock_existente.cantidad_m3            
# print("Actualizado stock existente")
    

# print("cread1")
    

class ActualizarStockRollizo(forms.ModelForm):
    exclude = ['fecha_crea']
    
    class Meta:
        
        model = StockRollizo
        fields = '__all__'

