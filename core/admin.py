from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.forms.widgets import MultiWidget
from .modelos.abastecimiento_rollizo import AbastecimientoRollizo 
from .modelos.bodega import Bodega
from .modelos.calidad_producto import CalidadProducto
from .modelos.costo_rollizo import CostoRollizo
from .modelos.costo_sobre_tiempo import CostoSobreTiempo
from .modelos.detalle_pedido import DetallePedido
from .modelos.empresa import Empresa
from .modelos.linea import Linea
from .modelos.linea_hh_disponible import LineaHhDisponible
from .modelos.patron_corte import PatronCorte
from .modelos.pedido import Pedido
from .modelos.periodo import Periodo
from .modelos.producto import Producto
from .modelos.producto_corte import ProductoCorte
from .modelos.productos_empresa import ProductosEmpresa
from .modelos.rollizo import Rollizo
from .modelos.rollizo_largo import RollizoLargo
from .modelos.stock_producto import StockProducto
from .modelos.stock_rollizo import StockRollizo
from .modelos.tiempo_cambio import TiempoCambio
from .modelos.tipo_periodo import TipoPeriodo
from .models import UserProfile

#EN PROCESO DE TOTAL CAMBIO

correction = 'width:100%;' #Estira un widget para ocultar comportamiento no buscado

class RutEmpresaWidget(MultiWidget):
    #rut empresa cómo rut body y rut dv
    def __init__(self, attrs=None):
        widgets = (
            #rut body
            forms.TextInput(attrs={'style': 'width: 10%; display: inline-block'}),
            #rut dv
            forms.TextInput(attrs={'style': 'width: 2%; display: inline-block'}),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            #se retorna el rut body y el rut dv en un array como value
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
    
class EmpresaForm(forms.ModelForm):
    rut_empresa = forms.CharField(widget=RutEmpresaWidget(), label='RUT Empresa')

    class Meta:
        model = Empresa
        fields = '__all__'
        
class BodegaAdminForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'
        widgets = {
            'rut_empresa': forms.Select(attrs={'style': correction}),
        }

class AbastecimientoRollizoAdminForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'
        widgets = {
            'id_rollizo': forms.Select(attrs={'style': correction}),
            'id_periodo': forms.Select(attrs={'style': correction}),
        }

class CostoRollizoAdminForm(forms.ModelForm):
    class Meta:
        model = CostoRollizo
        fields = '__all__'
        widgets = {
            'id_linea': forms.Select(attrs={'style': correction}),
            'rut_empresa': forms.Select(attrs={'style': correction}),
        }

class DetallePedidoAdminForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'
        widgets = {
            'id_pedido': forms.Select(attrs={'style': correction}),
            'id_producto': forms.Select(attrs={'style': correction}),
        }

class LineaHhDisponibleAdminForm(forms.ModelForm):
    class Meta:
        model = LineaHhDisponible
        fields = '__all__'
        widgets = {
            'id_linea': forms.Select(attrs={'style': correction}),
            'rut_empresa': forms.Select(attrs={'style': correction}),
        }

class PedidoAdminForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            'rut_empresa': forms.Select(attrs={'style': correction}),
        }

class PeriodoAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'id_tipo_periodo': forms.Select(attrs={'style': correction}),
        }

class ProductoAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'id_tipo_calidad': forms.Select(attrs={'style': correction}),
        }

class ProductoCorteAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'id_producto': forms.Select(attrs={'style': correction}),
            'id_patron': forms.Select(attrs={'style': correction}),
            'id_rollizo': forms.Select(attrs={'style': correction}),
        }

class ProductosEmpresaAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'id_producto': forms.Select(attrs={'style': correction}),
            'rut_empresa': forms.Select(attrs={'style': correction}),
        }

class RollizoAdminForm(forms.ModelForm):
    class Meta:
        model = Rollizo
        fields = '__all__'
        widgets = {
            'id_linea': forms.Select(attrs={'style': correction}),
            'id_largo': forms.Select(attrs={'style': correction}),
        }

class StockProductoAdminForm(forms.ModelForm):
    class Meta:
        model = StockProducto
        fields = '__all__'
        widgets = {
            'id_bodega': forms.Select(attrs={'style': correction}),
            'id_producto': forms.Select(attrs={'style': correction}),
        }

class TipoPeriodoAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'rut_empresa': forms.Select(attrs={'style': correction}),
        }

class TiempoCambioAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'id_linea': forms.Select(attrs={'style': correction}),
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
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()

    form = BodegaAdminForm
    list_display = ('nombre_bodega', 'descripcion_bodega')
    ordering = ('id_bodega',)
    readonly_fields = ('usuario_crea',)
    list_filter = ('rut_empresa__nombre_empresa',)

class EmpresaAdmin(admin.ModelAdmin):
    #Modelo administrador para empresa
    form = EmpresaForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    list_display = ('rut_empresa', 'nombre_empresa')
    ordering = ('rut_empresa',)
    readonly_fields = ('usuario_crea',)
    list_filter = (EstadoEmpresaFilter,)

class PatronCorteAdmin(admin.ModelAdmin):
    #Modelo administrador para pedido
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    list_display = ('nombre_patron', 'descripcion_patron')
    ordering = ('id_patron',)
    readonly_fields = ('usuario_crea',)

class PedidoAdmin(admin.ModelAdmin):
    #Modelo administrador para pedido
    form = PedidoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    list_display = ('numero_pedido', 'prioridad')
    ordering = ('id_pedido',)
    readonly_fields = ('usuario_crea',)
    list_filter = ('rut_empresa__nombre_empresa',)

class ProductoAdmin(admin.ModelAdmin):
    #Modelo administrador para producto
    form = ProductoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    list_display = ('nombre_producto', 'descripcion_producto')
    ordering = ('id_producto',)
    readonly_fields = ('usuario_crea',)
    list_filter = ('nombre_producto',)

class DetallePedidoAdmin(admin.ModelAdmin):
    form = DetallePedidoAdminForm
    list_display = ('get_producto','volumen_producto')
    def get_producto(self, obj):
        return obj.id_producto.nombre_producto
    ordering = ('id_detalle_pedido',)
    list_filter = ('id_pedido__rut_empresa__nombre_empresa','id_pedido__numero_pedido', 'id_producto__nombre_producto')
    get_producto.short_description = 'Producto'

class LineaAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    list_display = ('nombre_linea', 'descripcion_linea')
    ordering = ('nombre_linea',)
    readonly_fields = ('usuario_crea',)

class AbastecimientoRollizoAdmin(admin.ModelAdmin):
    form = AbastecimientoRollizoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

class CalidadProductoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

class CostoRollizoAdmin(admin.ModelAdmin):
    form = CostoRollizoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

class LineaHhDisponibleAdmin(admin.ModelAdmin):
    form = LineaHhDisponibleAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

class PeriodoAdmin(admin.ModelAdmin):
    form = PeriodoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

class ProductoCorteAdmin(admin.ModelAdmin):
    form = ProductoCorteAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

class ProductosEmpresaAdmin(admin.ModelAdmin):
    form = ProductosEmpresaAdminForm

class RollizoAdmin(admin.ModelAdmin):
    form = RollizoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

class StockProductoAdmin(admin.ModelAdmin):
    form = StockProductoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

class RollizoLargoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

class TiempoCambioAdmin(admin.ModelAdmin):
    form = TiempoCambioAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

class TipoPeriodoAdmin(admin.ModelAdmin):
    form = TipoPeriodoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.userprofile.rut
        obj.save()
    readonly_fields = ('usuario_crea',)

admin.site.register(AbastecimientoRollizo, AbastecimientoRollizoAdmin)
admin.site.register(Bodega, BodegaAdmin)
admin.site.register(DetallePedido, DetallePedidoAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Linea, LineaAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(PatronCorte, PatronCorteAdmin)
admin.site.register(CalidadProducto, CalidadProductoAdmin)
admin.site.register(CostoRollizo, CostoRollizoAdmin)
admin.site.register(LineaHhDisponible, LineaHhDisponibleAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ProductoCorte, ProductoCorteAdmin)
admin.site.register(ProductosEmpresa, ProductosEmpresaAdmin)
admin.site.register(Rollizo, RollizoAdmin)
admin.site.register(RollizoLargo, RollizoLargoAdmin)
admin.site.register(StockProducto, StockProductoAdmin)
admin.site.register(TiempoCambio, TiempoCambioAdmin)
admin.site.register(TipoPeriodo, TipoPeriodoAdmin)