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
from .modelos.productos_terminados import ProductoTerminado
from .modelos.stock_rollizo import StockRollizo
from .modelos.detalle_pedido import DetallePedido
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
            'orden_producto',
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
            'linea',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['linea'].queryset = Linea.objects.filter(eliminado=False)
        self.fields['nombre_rollizo'].queryset = Rollizo.objects.filter(eliminado=False)
        self.fields['patron_corte'].queryset = PatronCorte.objects.filter(eliminado=False)


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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['linea'].queryset = Linea.objects.filter(eliminado=False)

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empresa'].queryset = Empresa.objects.filter(eliminado=False)
        
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
    piezas =  forms.FloatField( min_value=0)
    volumen_producto =  forms.DecimalField(max_digits=10,min_value=0, decimal_places=3)
    mbf =  forms.DecimalField(max_digits=10,min_value=0, decimal_places=3)
    id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = DetallePedido

        fields = [
       
            'item',
            'mercado',
            'producto',
            'est',
            'term',
            'calidad',
            'alto_producto',
            'ancho_producto',
            'largo_producto',
            'piezas',
            'volumen_producto',
            'mbf',
            'banio',
            'marca',
            'puerto_destino',
            'programa',
            'cpo'
            #

        ]
      
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].widget = forms.Select(choices=Producto.objects.values_list('id', 'nombre'))
        self.fields['producto'].queryset = Producto.objects.filter(eliminado=False)

    def save(self, commit=True):
        instance = super().save(commit=False)
        producto = self.cleaned_data.get('producto')
        print(producto)
        if producto:

            # Access the id of the related Producto
            producto_id = producto.id
            print(producto_id)
            instance.detalle_producto = producto.nombre  # Fill detalle_producto with product name

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_entrega'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_produccion'].widget.attrs.update({'class': 'form-control'})


    class Meta:
         model = Pedido
         fields = [
             'cliente',
             'fecha_produccion',
             'fecha_entrega',
             'orden_interna',
             'comentario',
           #  'producto',
             'estado',
             'version'
         ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.filter(eliminado=False)

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
    exclude = ['fecha_crea']
    
    class Meta:
        model = StockProducto
        fields = '__all__'


class ActualizarStockRollizo(forms.ModelForm):
    exclude = ['fecha_crea']
    
    class Meta:
        
        model = StockRollizo
        fields = ['rollizo',
                  'cantidad',
                  'usuario_crea',
                  'bodega'] 


