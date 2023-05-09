from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.db.models import Q
from django.forms.widgets import TextInput
from django.forms.widgets import MultiWidget
from django.http import Http404
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from .modelos.abastecimiento_rollizo import AbastecimientoRollizo
from .modelos.bodega import Bodega
from .modelos.calidad_producto import CalidadProducto
from .modelos.cliente import Cliente
from .modelos.cliente_empresa import ClienteEmpresa
from .modelos.costo_rollizo import CostoRollizo
from .modelos.costo_sobre_tiempo import CostoSobreTiempo
from .modelos.detalle_pedido import DetallePedido
from .modelos.empresa import Empresa
from .modelos.inv_inicial_rollizo import InvInicialRollizo
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
from asignaciones.models import UserProfile
# Register your models here.
correction = 'width:100%;' #Estira un widget para ocultar comportamiento no buscado

class RutWidget(MultiWidget):
    '''Esta Clase nos da un widget para que el RUT sea más cómodo de ingresar en el admin'''
    #rut empresa cómo rut body y rut dv
    def __init__(self, attrs=None):
        widgets = (
            #rut body
            forms.TextInput(attrs={'style': 'width: 10%; display: inline-block', 'maxlength': '8'}),
            #rut dv
            forms.TextInput(attrs={'style': 'width: 2%; display: inline-block', 'maxlength': '1'}),
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
        #verifica si existe un valor en el input y si el atributo readonly ya se encuentra en la clase de los atributos
        readonly = value is not None and 'readonly' in attrs.get('class', '') 

        for i, widget in enumerate(self.widgets):
            widget_value = decompressed_value[i] if decompressed_value else None
            widget_attrs = attrs
            #agrega el atributo readonly solo si ya existe un valor en el input y si el atributo readonly no se encuentra ya en la clase de los atributos del widget
            if readonly and 'readonly' not in widget_attrs.get('class', ''): 
                widget_attrs['class'] = (widget_attrs.get('class', '') + ' readonly').strip()
            rendered_widgets.append(widget.render(f'{name}_{i}', widget_value, widget_attrs))
            if i == 0:
                rendered_widgets.append('<span> - </span>')

        return mark_safe(''.join(rendered_widgets))
    
    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return values[0] + '-' + values[1] if values[0] and values[1] else None

class TiempoCambioAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'linea': forms.Select(attrs={'style': correction}),
        }

class AbastecimientoRollizoAdminForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'
        widgets = {
            'rollizo': forms.Select(attrs={'style': correction}),
            'periodo': forms.Select(attrs={'style': correction,}),
        }
class AbastecimientoRollizoAdmin(admin.ModelAdmin):
    '''Administrador para el modelo de Abastecimiento Rollizo'''
    # cambio de apariencia
    form = AbastecimientoRollizoAdminForm
    # muestra tales columnas de la BD 
    list_display = ('id', 'numero_bloque', 'cantidad_hh')
    # usuario que crea no puede ser modificado
    readonly_fields = ('usuario_crea',)
    # se filtra por periodo
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('periodo__tipo_periodo__empresa__nombre_empresa',)
        else:
            return []
        
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        else:
            if obj:
                return [(None, {'fields': ('rollizo', 'periodo', 'numero_bloque', 'cantidad_hh', 'usuario_crea')})]
            else:
                return [(None, {'fields': ('rollizo', 'periodo', 'numero_bloque', 'cantidad_hh')})]
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las calidades producto
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las calidades producto por la empresa del usuario actual
            return queryset.filter(periodo__tipo_periodo__empresa=empresa)
    
    # filtra las claves foráneas para que sólo sean las de la empresa    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos las bodegas
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos las bodegas según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'rollizo':
            kwargs['queryset'] = Rollizo.objects.filter(linea__empresa=empresa)
        if db_field.name == 'periodo':
            kwargs['queryset'] = Periodo.objects.filter(tipo_periodo__empresa=empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    # guarda el usuario que crea la instancia
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

class BodegaAdminForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'
        widgets = {
            'empresa': forms.Select(attrs={'style': correction}),
        }

class BodegaAdmin(admin.ModelAdmin):
    # cambios en diseño
    form = BodegaAdminForm
    # muestra tales columnas de BD
    list_display = ('nombre_bodega', 'descripcion_bodega')
    # se ordena por id
    ordering = ('id',)
    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos bodega y descripcion_bodega
            return (
                (None, {'fields': ('nombre_bodega', 'descripcion_bodega')}),
            )
    # usuario que crea no puede ser cambiado
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['usuario_crea']
        else:
            return ['usuario_crea', 'empresa']
    # filtración por empresa
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('empresa__nombre_empresa',)
        else:
            return []
    # devuelve los sólo las bodegas pertenecientes a la empresa
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las bodegas
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las bodegas por la empresa del usuario actual
            return queryset.filter(empresa=empresa)
    # guarda usuario logueado
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        #si no es superusuario, aparte del rut guarda la empresa
        if not request.user.is_superuser:
            obj.empresa = request.user.empresa
        obj.save()

class CalidadProductoAdmin(admin.ModelAdmin):
    # se guarda usuario logueado
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        #si no es superusuario, aparte del rut guarda la empresa
        if not request.user.is_superuser:
            obj.empresa = request.user.empresa
        obj.save()
    # usuario que crea no puede ser cambiado
    readonly_fields = ('usuario_crea',)
    # filtración por empresa sólo para superusuarios
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('empresa__nombre_empresa',)
        else:
            return []
        
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        else:
            if obj:
                return [(None, {'fields': ('nombre_calidad', 'usuario_crea')})]
            else:
                return [(None, {'fields': ('nombre_calidad',)})]
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las calidades producto
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las calidades producto por la empresa del usuario actual
            return queryset.filter(empresa=empresa)

class ClienteForm(forms.ModelForm):
    rut_cliente = forms.CharField(widget=RutWidget(), label='RUT Cliente')

    class Meta:
        model = Cliente
        fields = '__all__'

class ClienteAdmin(admin.ModelAdmin):

    form = ClienteForm
    list_display = ('id', 'nombre_cliente')
    readonly_fields = ('usuario_crea',)

    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
        if not request.user.is_superuser:
            empresa = request.user.empresa
            cliente_empresa = ClienteEmpresa.objects.filter(cliente=obj, empresa=empresa).first()
            if not cliente_empresa:
                cliente_empresa = ClienteEmpresa(cliente=obj, empresa=empresa)
                cliente_empresa.save()

    # devuelve sólo los clientes pertenecientes a la empresa
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas los clientes
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar los clientes por la empresa del usuario actual
            return queryset.filter(empresa=empresa)
        
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('empresa__nombre_empresa',)
        else:
            return []
        
    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos bodega y descripcion_bodega
            return (
                (None, {'fields': ('rut_cliente', 'nombre_cliente', 'correo_cliente', 'estado_cliente', 'fecha_vigencia', 'nombre_fantasia', 'ciudad', 'telefono')}),
            )


class CostoRollizoAdminForm(forms.ModelForm):
    class Meta:
        model = CostoRollizo
        fields = '__all__'
        widgets = {
            'linea': forms.Select(attrs={'style': correction}),
            'empresa': forms.Select(attrs={'style': correction}),
        }

class CostoRollizoAdmin(admin.ModelAdmin):
    # cambios en diseño
    form = CostoRollizoAdminForm
    # se guarda usuario logueado
    list_display = ('nombre_costo', 'valor_m3')
    ordering = ('nombre_costo',)
    # no se puede cambiar usuario que crea
    readonly_fields = ('usuario_crea',)
    # filtración por empresa sólo para superusuarios
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('empresa__nombre_empresa',)
        else:
            return []
        
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['usuario_crea']
        else:
            return ['usuario_crea', 'empresa']
        
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        else:
            if obj:
                return [(None, {'fields': ('nombre_costo', 'valor_m3', 'linea', 'empresa', 'usuario_crea')})]
            else:
                return [(None, {'fields': ('nombre_costo', 'valor_m3', 'linea')})]
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las calidades producto
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las calidades producto por la empresa del usuario actual
            return queryset.filter(empresa=empresa)
        
    # filtra las claves foráneas para que sólo sean las de la empresa    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos las bodegas
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos las bodegas según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'linea':
            kwargs['queryset'] = Linea.objects.filter(empresa=empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
    # se guarda usuario logueado
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        #si no es superusuario, aparte del rut guarda la empresa
        if not request.user.is_superuser:
            obj.empresa = request.user.empresa
        obj.save()

class CostoSobreTiempoAdmin(admin.ModelAdmin):
    # filtración por empresa sólo para superusuarios
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('empresa__nombre_empresa',)
        else:
            return []
        
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['usuario_crea']
        else:
            return ['usuario_crea', 'empresa']
        
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        else:
            if obj:
                return [(None, {'fields': ('valor', 'empresa', 'usuario_crea')})]
            else:
                return [(None, {'fields': ('valor',)})]
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las calidades producto
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las calidades producto por la empresa del usuario actual
            return queryset.filter(empresa=empresa)
        
    # se guarda usuario logueado
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        #si no es superusuario, aparte del rut guarda la empresa
        if not request.user.is_superuser:
            obj.empresa = request.user.empresa
        obj.save()

class ProductoInline(admin.TabularInline):
    model = Empresa.productos.through
    extra = 1
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj=obj)
        else:
            return [f.name for f in self.model._meta.fields]

class ClienteInline(admin.TabularInline):
    model = Empresa.cliente.through
    extra = 1
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj=obj)
        else:
            return [f.name for f in self.model._meta.fields]

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

class EmpresaForm(forms.ModelForm):
    rut_empresa = forms.CharField(widget=RutWidget(), label='RUT Empresa')

    class Meta:
        model = Empresa
        fields = '__all__'

class EmpresaAdmin(admin.ModelAdmin):
    #Modelo administrador para empresa
    def has_permission(self, request):
        # Verificar si el usuario es un superusuario
        return request.user.is_superuser
    form = EmpresaForm
    inlines = (ProductoInline, ClienteInline)
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('__str__', 'rut_empresa')
    ordering = ('nombre_empresa',)
    list_filter = (EstadoEmpresaFilter,)
    # devuelve sólo empresa
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las empresas
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Admin sólo puede ver su empresa
            return queryset.filter(rut_empresa=empresa.rut_empresa)
        
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['usuario_crea']
        else:
            return ['rut_empresa', 'usuario_crea']

class InvInicialRollizoAdmin(admin.ModelAdmin):
    readonly_fields = ('usuario_crea',)
    # Obtiene los campos necesarios para cada caso
    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos bodega y descripcion_bodega
            return (
                (None, {'fields': ('nombre_inventario', 'descripcion_inventario', 'diametro', 'cant_m3', 'bodega')}),
            )
    # filtración por empresa
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('bodega__empresa__nombre_empresa',)
        else:
            return []
    # devuelve los sólo las bodegas pertenecientes a la empresa
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las bodegas
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las bodegas por la empresa del usuario actual
            return queryset.filter(bodega__empresa=empresa)

    # filtra las claves foráneas para que sólo sean las de la empresa    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos las bodegas
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos las bodegas según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'bodega':
            kwargs['queryset'] = Bodega.objects.filter(empresa=empresa)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

class LineaAdmin(admin.ModelAdmin):

    list_display = ('nombre_linea', 'descripcion_linea')
    ordering = ('nombre_linea',)
    readonly_fields = ('usuario_crea',)
    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos bodega y descripcion_bodega
            return (
                (None, {'fields': ('nombre_linea', 'descripcion_linea')}),
            )
    # usuario que crea no puede ser cambiado
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['usuario_crea']
        else:
            return ['usuario_crea', 'empresa']
    # filtración por empresa
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('empresa__nombre_empresa',)
        else:
            return []
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las bodegas
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las bodegas por la empresa del usuario actual
            return queryset.filter(empresa=empresa)
        
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.empresa = request.user.empresa
        obj.save()

class LineaHhDisponibleAdminForm(forms.ModelForm):
    class Meta:
        model = LineaHhDisponible
        fields = '__all__'
        widgets = {
            'linea': forms.Select(attrs={'style': correction}),
            'empresa': forms.Select(attrs={'style': correction}),
        }

class LineaHhDisponibleAdmin(admin.ModelAdmin):
    form = LineaHhDisponibleAdminForm
    list_display = ('id', 'numero_bloque')
    readonly_fields = ('usuario_crea',)
    list_filter = ('empresa__nombre_empresa',)

    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos bodega y descripcion_bodega
            return (
                (None, {'fields': ('linea', 'numero_bloque', 'cantidad_hh')}),
            )
    # usuario que crea no puede ser cambiado, mismo con empresa
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['usuario_crea']
        else:
            return ['usuario_crea', 'empresa']

    # filtración por empresa
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('empresa__nombre_empresa',)
        else:
            return []
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las bodegas
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las bodegas por la empresa del usuario actual
            return queryset.filter(empresa=empresa)
        
    # filtra las claves foráneas para que sólo sean las de la empresa    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos las bodegas
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos las bodegas según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'linea':
            kwargs['queryset'] = Linea.objects.filter(empresa=empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        if not request.user.is_superuser:
            obj.empresa = request.user.empresa
        obj.save()

class PatronCorteAdmin(admin.ModelAdmin):
    #Modelo administrador para pedido
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('nombre_patron', 'descripcion_patron')
    ordering = ('id',)
    readonly_fields = ('usuario_crea',)
    list_filter = ('productocorte__producto__productosempresa__empresa__nombre_empresa',)

class DetalleProductoInline(admin.TabularInline):
    model = Pedido.productos.through
    extra = 1
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos los productos
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos los productos según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'producto':
            kwargs['queryset'] = Producto.objects.filter(empresa=empresa)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PedidoAdminForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            'empresa': forms.Select(attrs={'style': correction}),
        }

class PedidoAdmin(admin.ModelAdmin):
    #Modelo administrador para pedido
    form = PedidoAdminForm
    inlines = (DetalleProductoInline,)
    list_display = ('numero_pedido', 'prioridad',)
    ordering = ('id',)
    readonly_fields = ('usuario_crea',)

    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "cliente":
            # Filtra los clientes por la empresa correspondiente al usuario actual
            kwargs["queryset"] = Cliente.objects.filter(empresa=request.user.empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('cliente__empresa__nombre_empresa',)
        else:
            return []

class PeriodoAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'tipo_periodo': forms.Select(attrs={'style': correction}),
        }
        
class PeriodoAdmin(admin.ModelAdmin):
    form = PeriodoAdminForm
    list_display = ('nombre_periodo', 'descripcion_periodo', 'cantidad_periodos')
    readonly_fields = ('usuario_crea',)
    # filtración por empresa sólo para superusuarios
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('tipo_periodo__empresa__nombre_empresa',)
        else:
            return []
    # devuelve los sólo los tipo periodo pertenecientes a la empresa
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas los tipo periodo
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las tipo periodo por la empresa del usuario actual
            return queryset.filter(tipo_periodo__empresa=empresa)
        
    # filtra las claves foráneas para que sólo sean las de la empresa    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos las bodegas
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos las bodegas según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'tipo_periodo':
            kwargs['queryset'] = TipoPeriodo.objects.filter(empresa=empresa)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

class ProductoAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'tipo_calidad': forms.Select(attrs={'style': correction}),
        }

class ProductoAdmin(admin.ModelAdmin):
    #Modelo administrador para producto
    form = ProductoAdminForm
    list_display = ('nombre_producto', 'descripcion_producto')
    ordering = ('id',)
    readonly_fields = ('usuario_crea',)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas los productos
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar los productos por la empresa del usuario actual
            return queryset.filter(empresa=empresa)
    
    #Si es superusuario puede filtrar por empresa, si no no
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('productosempresa__empresa__nombre_empresa',)
        else:
            return []
        
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
        #Si no es superusuario, el producto a guardar se asocia a la empresa
        empresa = request.user.empresa
        producto_empresa = ProductosEmpresa.objects.filter(producto=obj, empresa=empresa).first()
        if not producto_empresa:
            # Si no existe, crear una nueva instancia y guardarla
            producto_empresa = ProductosEmpresa(producto=obj, empresa=empresa)
            producto_empresa.save()

class ProductoCorteAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'producto': forms.Select(attrs={'style': correction}),
            'patron': forms.Select(attrs={'style': correction}),
            'rollizo': forms.Select(attrs={'style': correction}),
        }

class ProductoCorteAdmin(admin.ModelAdmin):
    form = ProductoCorteAdminForm
    list_display = ('cantidad_producto', 'descripcion_corte')
    readonly_fields = ('usuario_crea',)
    #Cambia los campos que se muestran
    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos bodega y descripcion_bodega
            return (
                (None, {'fields': ('producto', 'patron', 'cantidad_producto', 'descripcion_corte', 'rollizo')
}),
            )
    # filtra los resultados
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las bodegas
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las bodegas por la empresa del usuario actual
            return queryset.filter(producto__empresa=empresa)
        
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('producto__empresa__nombre_empresa',)
        else:
            return []
        
     # filtra las claves foráneas para que sólo sean las de la empresa    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos las bodegas
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos las bodegas según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'producto':
            kwargs['queryset'] = Producto.objects.filter(empresa=empresa)
        if db_field.name == 'rollizo':
            kwargs['queryset'] = Rollizo.objects.filter(linea__empresa=empresa)
        if db_field.name == 'patron_corte':
            kwargs['queryset'] = PatronCorte.objects.filter(empresa=empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

class ProductosEmpresaAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'producto': forms.Select(attrs={'style': correction}),
            'empresa': forms.Select(attrs={'style': correction}),
        }

class ProductosEmpresaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'producto')
    form = ProductosEmpresaAdminForm
    list_filter = ('empresa__nombre_empresa', 'producto__nombre_producto')

class RollizoAdminForm(forms.ModelForm):
    class Meta:
        model = Rollizo
        fields = '__all__'
        widgets = {
            'linea': forms.Select(attrs={'style': correction}),
            'rollizo_largo': forms.Select(attrs={'style': correction}),
        }

class LineaFilter(admin.SimpleListFilter):
    title = 'Linea'
    parameter_name = 'linea'

    def lookups(self, request, model_admin):
        empresa = request.user.empresa
        lineas = Linea.objects.filter(empresa=empresa)
        return [(linea.id, linea.nombre_linea) for linea in lineas]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(linea__id=self.value())

class RollizoAdmin(admin.ModelAdmin):
    form = RollizoAdminForm
    list_display = ('nombre_rollizo', 'descripcion_rollizo', 'linea')
    readonly_fields = ('usuario_crea',)

    #Cambia los campos que se muestran
    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos bodega y descripcion_bodega
            return (
                (None, {'fields': ('nombre_rollizo', 'descripcion_rollizo', 'linea', 'diametro', 'rollizo_largo', 'clase_diametrica')
}),
            )

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('rollizo_largo__empresa__nombre_empresa','linea__nombre_linea')
        else:
            return (LineaFilter,)
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las bodegas
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las bodegas por la empresa del usuario actual
            return queryset.filter(rollizo_largo__empresa=empresa)
        
    # filtra las claves foráneas para que sólo sean las de la empresa    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos las bodegas
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos las bodegas según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'linea':
            kwargs['queryset'] = Linea.objects.filter(empresa=empresa)
        if db_field.name == 'rollizo_largo':
            kwargs['queryset'] = RollizoLargo.objects.filter(empresa=empresa)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()


class RollizoLargoAdmin(admin.ModelAdmin):
    list_display = ('nombre_largo', 'descripcion_largo')
    readonly_fields = ('usuario_crea',)
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('empresa__nombre_empresa',)
        else:
            return []
        
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['usuario_crea']
        else:
            return ['usuario_crea', 'empresa']
        
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        else:
            if obj:
                return [(None, {'fields': ('nombre_largo', 'descripcion_largo', 'largo', 'empresa', 'usuario_crea')})]
            else:
                return [(None, {'fields': ('nombre_largo', 'descripcion_largo', 'largo',)})]
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las calidades producto
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las calidades producto por la empresa del usuario actual
            return queryset.filter(empresa=empresa)
        
    # se guarda usuario logueado
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        #si no es superusuario, aparte del rut guarda la empresa
        if not request.user.is_superuser:
            obj.empresa = request.user.empresa
        obj.save()


#Filtro custom para filtrar sólo las bodegas correspondientes a la empresa
class BodegaFilter(admin.SimpleListFilter):
    title = 'Bodega'
    parameter_name = 'bodega'

    def lookups(self, request, model_admin):
        empresa = request.user.empresa
        bodegas = Bodega.objects.filter(empresa=empresa)
        return [(bodega.id, bodega.nombre_bodega) for bodega in bodegas]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(bodega__id=self.value())

class StockProductoAdminForm(forms.ModelForm):
    class Meta:
        model = StockProducto
        fields = '__all__'
        widgets = {
            'bodega': forms.Select(attrs={'style': correction}),
            'producto': forms.Select(attrs={'style': correction}),
        }

class StockProductoAdmin(admin.ModelAdmin):
    form = StockProductoAdminForm
    list_display = ('producto', 'cantidad_m3', 'bodega')
    readonly_fields = ('usuario_crea',)
    
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('bodega__empresa__nombre_empresa', 'bodega__nombre_bodega')
        else:
            return (BodegaFilter,)
        
    # devuelve los sólo los stock de bodega pertenecientes a la empresa
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todos los stock de bodega
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar los stock de bodega por la empresa del usuario actual
            return queryset.filter(bodega__empresa=empresa)
        
    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos bodega y descripcion_bodega
            return (
                (None, {'fields': ('bodega', 'producto', 'cantidad_m3')}),
            )    
    
    # filtra las claves foráneas para que sólo sean las de la empresa    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos las bodegas
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos las bodegas según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'bodega':
            kwargs['queryset'] = Bodega.objects.filter(empresa=empresa)
        if db_field.name == 'producto':
            kwargs['queryset'] = Producto.objects.filter(empresa=empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

class StockRollizoAdmin(admin.ModelAdmin):
    list_display = ('rollizo', 'cantidad', 'bodega')
    readonly_fields = ('usuario_crea',)
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('bodega__empresa__nombre_empresa', 'bodega__nombre_bodega')
        else:
            return (BodegaFilter,)
        
    # devuelve los sólo los stock de bodega pertenecientes a la empresa
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todos los stock de bodega
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar los stock de bodega por la empresa del usuario actual
            return queryset.filter(bodega__empresa=empresa)
        
    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos bodega y descripcion_bodega
            return (
                (None, {'fields': ('rollizo', 'cantidad', 'bodega')}),
            )    
    
    # filtra las claves foráneas para que sólo sean las de la empresa    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos las bodegas
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos las bodegas según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'bodega':
            kwargs['queryset'] = Bodega.objects.filter(empresa=empresa)
        if db_field.name == 'rollizo':
            kwargs['queryset'] = Rollizo.objects.filter(linea__empresa=empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

class TiempoCambioAdmin(admin.ModelAdmin):
    form = TiempoCambioAdminForm
    readonly_fields = ('usuario_crea',)
    #Cambia los campos que se muestran
    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos valor y linea
            return (
                (None, {'fields': ('valor', 'linea')}),
            )
    # filtración por empresa
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('costosobretiempo__empresa__nombre_empresa',)
        else:
            return []
    
    # filtra los resultados
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas los tiempo cambio
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar los tiempo cambio por la empresa del usuario actual
            return queryset.filter(costosobretiempo__empresa=empresa)
    
    # filtra las claves foráneas para que sólo sean las de la empresa    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario es superusuario, no filtramos los tiempo cambio
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Filtramos las bodegas según la empresa del usuario actual
        empresa = request.user.empresa
        if db_field.name == 'linea':
            kwargs['queryset'] = Linea.objects.filter(empresa=empresa)
        if db_field.name == 'costosobretiempo':
            kwargs['queryset'] = CostoSobreTiempo.objects.filter(empresa=empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

class TipoPeriodoAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'empresa': forms.Select(attrs={'style': correction}),
        }

class TipoPeriodoAdmin(admin.ModelAdmin):
    form = TipoPeriodoAdminForm
    list_display = ('__str__',)
    readonly_fields = ('usuario_crea',)
    list_filter = ('empresa__nombre_empresa',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['usuario_crea']
        else:
            return ['usuario_crea', 'empresa']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('empresa__nombre_empresa',)
        else:
            return []    
        
    # obtiene los campos necesarios para cada caso
    def get_fieldsets(self, request, obj=None):
        if obj or request.user.is_superuser:
            # Superusuarios pueden editar todos los campos
            return super().get_fieldsets(request, obj)
        else:
            # Usuarios no superusuarios solo pueden ver los campos bodega y descripcion_bodega
            return (
                (None, {'fields': ('nombre_tipo_periodo', 'descripcion_tipo_periodo', 'dias')}),
            )
        
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todas las calidades producto
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar las calidades producto por la empresa del usuario actual
            return queryset.filter(empresa=empresa)
    
    # guarda usuario logueado
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        if not request.user.is_superuser:
            obj.empresa = request.user.empresa
        obj.save()

class UserProfileCreationForm(UserCreationForm):
    rut = forms.CharField(widget=RutWidget(), label='RUT')

    class Meta:
        model = UserProfile
        fields = ('username', 'rut', 'empresa')
        help_texts = {
            'username': '30 caracteres o menos. Letras, números y @/./+/-/_ solamente.',
            'password1': '<ul class="password-help"><li>La contraseña no puede ser demasiado similar a su otro información personal.</li><li>La contraseña debe contener al menos 8 caracteres.</li><li>La contraseña no puede ser una contraseña comúnmente utilizada.</li><li>La contraseña no puede ser completamente numérica.</li></ul>',
            'rut': 'Ingrese su rut',
            'empresa': 'Ingrese su empresa'
        }

class UserProfileAdmin(UserAdmin):
    add_form = UserProfileCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'rut', 'empresa', 'email', 'password1', 'password2',),
        }),
    )
    #form = UserProfileChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'rut', 'empresa')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    def get_fieldsets(self, request, obj=None):
        # Si se quiere editar
        if obj is not None and not request.user.is_superuser:
            # Usuarios no superusuarios no pueden editar el campo is_superuser
            return (
                (None, {'fields': ('username', 'password')}),
                (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'rut', 'empresa')}),
                (('Permissions'), {'fields': ('groups',)}),
                (('Important dates'), {'fields': ('last_login', 'date_joined')}),
            )
        if obj is None and not request.user.is_superuser:
            return(None, {
                'classes': ('wide',),
                'fields': ('username', 'rut', 'email', 'password1', 'password2', ),
            }),
        else:
            return super().get_fieldsets(request, obj)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(empresa=request.user.empresa)
            qs = qs.exclude(is_superuser=True)
        return qs
    
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['empresa']
        return []
    
    def get_list_filter(self, request):
        if not request.user.is_superuser:
            return ['is_active', 'is_staff']
        return super().get_list_filter(request)
    
    # guarda usuario logueado
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        if not request.user.is_superuser:
            obj.empresa = request.user.empresa
        obj.save()

    

admin.site.register(AbastecimientoRollizo, AbastecimientoRollizoAdmin)
admin.site.register(Bodega, BodegaAdmin)
admin.site.register(CalidadProducto, CalidadProductoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(CostoRollizo, CostoRollizoAdmin)
admin.site.register(CostoSobreTiempo, CostoSobreTiempoAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(InvInicialRollizo, InvInicialRollizoAdmin)
admin.site.register(Linea, LineaAdmin)
admin.site.register(LineaHhDisponible, LineaHhDisponibleAdmin)
admin.site.register(PatronCorte, PatronCorteAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ProductoCorte, ProductoCorteAdmin)
admin.site.register(Rollizo, RollizoAdmin)
admin.site.register(RollizoLargo, RollizoLargoAdmin)
admin.site.register(StockProducto, StockProductoAdmin)
admin.site.register(StockRollizo, StockRollizoAdmin)
admin.site.register(TiempoCambio, TiempoCambioAdmin)
admin.site.register(TipoPeriodo, TipoPeriodoAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
