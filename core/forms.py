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
from .modelos.empresa import Empresa
from .modelos.productos_terminados import ProductoTerminado
from .modelos.detalle_pedido import DetallePedido
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from datetime import date
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

class ActualizarMateriaPrimaForm(forms.ModelForm):
    """Esta clase permite actualizar la materia prima de la vista de 'Materia Prima'"""
    numero_buzon =forms.FloatField(min_value=0)
    largo =forms.FloatField(min_value=0)
    cantidad =forms.FloatField(min_value=0)
    numero_buzon =forms.FloatField(min_value=0)
    costo_almacenamiento =forms.FloatField(min_value=0)
    inventario_inicial =forms.FloatField(min_value=0)
    volumen_procesado =forms.FloatField(min_value=0)
    inventario_final =forms.FloatField(min_value=0)
    class Meta:
        model = MateriaPrima
        fields = [
            'numero_buzon',
            'tipo_madera',
            'clase_diametrica',
            'largo',
            'cantidad',
            'conicidad',
            #'linea_produccion',
            'costo_almacenamiento',
            'inventario_inicial',
            'volumen_procesado',
            'inventario_final',
        ]

class CrearPatronCorteForm(forms.ModelForm):
    """Esta clase permite crear un nuevo patrón de corte"""
    ##Validaciones 
    rendimiento = forms.FloatField(min_value=0,max_value=2000)
    velocidad_linea = forms.FloatField(min_value=0,max_value=2000)
    setup_time = forms.FloatField(min_value=0,max_value=2000)
    lead_time = forms.FloatField(min_value=0,max_value=2000)
    class Meta:
        model = PatronCorte
        fields = [
            'codigo',
            'nombre',
            'descripcion',
            'rollizo',
            'rendimiento',
            'velocidad_linea',
            'setup_time',
            'lead_time',
            'utilizado',
            'producto_asociado',
        ]

 
class CrearProductoForm(forms.ModelForm):
    """Esta clase permite crear un nuevo producto"""
    alto = forms.FloatField(min_value=0)
    ancho = forms.FloatField(min_value=0)
    largo = forms.FloatField(min_value=0)
    inventario_inicial = forms.FloatField(min_value=0)
    inventario_final = forms.FloatField(min_value=0)
    
    class Meta:
        model = Producto
        fields = [
            'codigo',
            'nombre',
            'descripcion',
            'largo',
            'ancho',
            'alto',
            'inventario_inicial',
            'valor_inventario',
            'costo_almacenamiento',
            'nombre_rollizo',
            'inventario_final',
            'patron_corte',
            'linea'
        ]
#Lista valores prioridad
# class DetallePedidoForm(forms.ModelForm):

#     class Meta:
#         model = DetallePedido
#         fields = [
    
#             'detalle_producto',
#             'alto_producto',
#             'ancho_producto',
#             'largo_producto',
#             'volumen_producto',
#             'fecha_entrega',
#             'estado_pedido_linea',
#             #'grado_urgencia',
#             'cantidad_piezas',
#             'cantidad_trozos',
#             'piezas_xpaquete',
#             'piezas_xtrozo',
#             'paquetes_solicitados',
#             'volumen_obtenido',
#             'paquetes_saldo',

#         ]

class DetallePedidoForm(forms.ModelForm):

    class Meta:
        model = DetallePedido
        fields = [
            'producto',
            'detalle_producto',
            'alto_producto',
            'ancho_producto',
            'largo_producto',
            'volumen_producto',
            #'fecha_entrega',
            'estado_pedido_linea',
            'cantidad_piezas',
            'cantidad_trozos',
            'piezas_xpaquete',
            'piezas_xtrozo',
            'paquetes_solicitados',
            'volumen_obtenido',
            'paquetes_saldo',
            'grado_urgencia'
            # Add other fields here
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the widget for the producto field to a Select widget
        self.fields['producto'].widget = forms.Select(choices=Producto.objects.values_list('id', 'id'))
        #self.fields['producto'].widget = forms.SelectMultiple(choices=Producto.objects.values_list('id', 'id'))

class CrearRollizoForm(forms.ModelForm):
    exclude = ['fecha_crea']
    class Meta:
        model = Rollizo
        fields =[
            'nombre_rollizo',
            'descripcion_rollizo',
            'linea',
            'diametro',
            'largo',
            'usuario_crea',
            'clase_diametrica'
        ]
        
        

class CrearLineaForm(forms.ModelForm):
    exclude = ['fecha_crea']
    class Meta:
        model = Linea
        fields =[
            'nombre_linea',
            'descripcion_linea',
            'empresa',
            'usuario_crea'       
        ]
        
        
class CrearClienteForm(forms.ModelForm):
    exclude = ['fecha_crea']
    class Meta:
        model = Cliente
        fields =[      
                 'rut_cliente',
                 'nombre_cliente',
                 'correo_cliente',
                 'usuario_crea',
                 'ciudad',
                 'telefono',
                 'mercado',
                 'puerto_destino'
        ]
        
class CrearEmpresaForm(forms.ModelForm):
    exclude = ['fecha_crea']
    class Meta:
        model = Empresa
        fields =[    
                 'rut_empresa',
                 'nombre_empresa',
                 'correo_empresa',
                 'estado_empresa',
                 'fecha_vigencia',
                 'usuario_crea',
                 'nombre_fantasia',
                 'ciudad',
                 'telefono',
                 'productos',
                 'cliente',
        ]


class ActualizarPedidoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['fecha_entrega'].widget = forms.widgets.DateInput(
             attrs={
                 'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                 'class': 'form-control'
             }
         )

         self.fields['fecha_produccion'].widget = forms.widgets.DateInput(
             attrs={
                 'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                 'class': 'form-control'
             }
         )

    class Meta:
         model = Pedido
         fields = [
             'cliente',
             'fecha_produccion',
             'fecha_entrega',
             'orden_pedido',
             'comentario',
           #  'producto',
             'prioridad',
             'estado',
             'version'
         ]
         

DetallePedidoFormSet = inlineformset_factory(
    Pedido,  # Parent model
    DetallePedido,  # Child model
    form=DetallePedidoForm,  # Use the modified DetallePedidoForm
    extra=1,  # Number of empty forms to display
    can_delete=True,  # Allow formset to delete records
)


   

class ProductoTerminadoForm(forms.ModelForm):
    """Esta clase permite crear un nuevo producto terminado"""
    class Meta:
        model = ProductoTerminado
        fields = ['codigo', 'nombre', 'grosor', 'ancho', 'largo', 'clase_diametrica', 'patron_corte', 'cantidad_producida', 'fecha_produccion']
