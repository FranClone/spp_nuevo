from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.forms.widgets import MultiWidget
from .modelos.bodega import Bodega
from .modelos.empresa import Empresa
from .modelos.linea import Linea
from .modelos.pedido import Pedido
from .modelos.producto import Producto
from .modelos.detalle_pedido import DetallePedido
from .models import UserProfile

#EN PROCESO DE TOTAL CAMBIO

class RutForm(forms.ModelForm):
    #este método chequea que el rut, ya sea de empresa o persona, sea válido
    def clean_rut(self, is_empresa=False):
        #obtiene los datos
        cleaned_data = super().clean()
        #datos del rut
        rut_body = cleaned_data.get("rut_body")
        rut_dv = cleaned_data.get("rut_dv")
        if is_empresa:
            #datos del rut de la empresa
            rut_body = cleaned_data.get("rut_empresa_body")
            rut_dv = cleaned_data.get("rut_empresa_dv")
        rut = f"{rut_body}-{rut_dv}"

        #si existe
        if rut_body and rut_dv:
            #ve si el rut son solo dígitos y hace el cálculo del rutificador
            def validate_rut(rut):
                rut = str(rut)
                rut = rut.replace("-", "")
                if not rut.isdigit() and rut[-1].upper() != 'K':
                    raise ValidationError('El RUT solo puede contener números y un guión')
                if len(rut) < 8:
                    raise ValidationError('El RUT es demasiado corto')
                #aquí empieza el algoritmo módulo 11
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

            #valida el rut
            try:
                validate_rut(rut)
            except ValidationError as e:
                raise forms.ValidationError(e)

            #retorna el rut
            cleaned_data["rut" if not is_empresa else "rut_empresa"] = rut

        return cleaned_data

class RutEmpresaWidget(MultiWidget):
    #inicializa el widget
    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(attrs={'style': 'width: 10%; display: inline-block'}),
            forms.TextInput(attrs={'style': 'width: 2%; display: inline-block'}),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value[:-2], value[-1]]
        return [None, None]
    
    def render(self, name, value, attrs=None, renderer=None):
        rendered_widgets = []
        decompressed_value = self.decompress(value)
        for i, widget in enumerate(self.widgets):
            widget_value = decompressed_value[i] if decompressed_value else None
            rendered_widgets.append(widget.render(f'{name}_{i}', widget_value, attrs))
            if i == 0:
                rendered_widgets.append('<span> - </span>')
        return mark_safe(''.join(rendered_widgets))
    
    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return values[0] + '-' + values[1] if values[0] and values[1] else None
    
class EmpresaForm(RutForm):
    rut_empresa = forms.CharField(widget=RutEmpresaWidget(), label='RUT Empresa')

    class Meta:
        model = Empresa
        fields = '__all__'
        
class BodegaAdminForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'
        widgets = {
            'rut_empresa': forms.Select(attrs={'style': 'width:100%;'}),
        }

class DetallePedidoAdminForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'
        widgets = {
            'id_pedido': forms.Select(attrs={'style': 'width:100%;'}),
            'id_producto': forms.Select(attrs={'style': 'width:100%;'}),
        }

class EstadoEmpresaFilter(admin.SimpleListFilter):
    #Este filtro, reemplaza los 0s y 1s de estado por Activo e Inactivo
    title = 'Estado'
    parameter_name = 'estado'

    #El filtro se muestra por activo e inactivo
    def lookups(self, request, model_admin):
        return (
            ('activo', 'Activo'),
            ('inactivo', 'Inactivo'),
        )
    #Si se selecciona activo, busca los 1, si no, los 0
    def queryset(self, request, queryset):
        if self.value() == 'activo':
            return queryset.filter(estado_empresa=True)
        elif self.value() == 'inactivo':
            return queryset.filter(estado_empresa=False)
        else:
            return queryset

class UserAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_nombre_empresa')
    ordering = ('user__id',)
    def get_username(self, obj):
        return obj.user.username
    def get_nombre_empresa(self, obj):
        return obj.rut_empresa.nombre_empresa

    get_username.short_description = 'Nombre de Usuario'
    get_nombre_empresa.short_description = 'Empresa'

class BodegaAdmin(admin.ModelAdmin):
    form = BodegaAdminForm
    list_display = ('nombre_bodega', 'descripcion_bodega')
    ordering = ('id_bodega',)
    list_filter = ('rut_empresa__nombre_empresa',)

class EmpresaAdmin(admin.ModelAdmin):
    #Modelo administrador para empresa
    form = EmpresaForm
    list_display = ('rut_empresa', 'nombre_empresa')
    ordering = ('rut_empresa',)
    list_filter = (EstadoEmpresaFilter,)

class PedidoAdmin(admin.ModelAdmin):
    #Modelo administrador para pedido
    list_display = ('numero_pedido', 'prioridad')
    ordering = ('id_pedido',)
    list_filter = ('rut_empresa__nombre_empresa',)

class ProductoAdmin(admin.ModelAdmin):
    #Modelo administrador para producto
    list_display = ('nombre_producto', 'descripcion_producto')
    ordering = ('id_producto',)
    list_filter = ('rut_empresa__nombre_empresa', 'nombre_producto')

class DetallePedidoAdmin(admin.ModelAdmin):
    form = DetallePedidoAdminForm
    list_display = ('get_producto','volumen_producto')
    def get_producto(self, obj):
        return obj.id_producto.nombre_producto
    ordering = ('id_detalle_pedido',)
    list_filter = ('id_pedido__rut_empresa__nombre_empresa','id_pedido__numero_pedido', 'id_producto__nombre_producto')
    get_producto.short_description = 'Producto'

class LineaAdmin(admin.ModelAdmin):
    list_display = ('nombre_linea', 'descripcion_linea')
    ordering = ('nombre_linea',)
    list_filter = ('rut_empresa__nombre_empresa', )

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Bodega, BodegaAdmin)
admin.site.register(DetallePedido, DetallePedidoAdmin)
admin.site.register(Linea, LineaAdmin)
admin.site.register(UserProfile, UserAdmin)