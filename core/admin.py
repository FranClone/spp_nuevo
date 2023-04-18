from django import forms
from django.contrib import admin
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

class DetalleProductoInline(admin.TabularInline):
    model = Pedido.productos.through
    extra = 1

class ProductoInline(admin.TabularInline):
    model = Empresa.productos.through
    extra = 1

class RutWidget(MultiWidget):
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
        readonly = value is not None and 'readonly' in attrs.get('class', '') #verifica si existe un valor en el input y si el atributo readonly ya se encuentra en la clase de los atributos

        for i, widget in enumerate(self.widgets):
            widget_value = decompressed_value[i] if decompressed_value else None
            widget_attrs = attrs
            if readonly and 'readonly' not in widget_attrs.get('class', ''): #agrega el atributo readonly solo si ya existe un valor en el input y si el atributo readonly no se encuentra ya en la clase de los atributos del widget
                widget_attrs['class'] = (widget_attrs.get('class', '') + ' readonly').strip()
            rendered_widgets.append(widget.render(f'{name}_{i}', widget_value, widget_attrs))
            if i == 0:
                rendered_widgets.append('<span> - </span>')

        return mark_safe(''.join(rendered_widgets))
    
    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        return values[0] + '-' + values[1] if values[0] and values[1] else None

class EmpresaForm(forms.ModelForm):
    rut_empresa = forms.CharField(widget=RutWidget(), label='RUT Empresa')

    class Meta:
        model = Empresa
        fields = '__all__'
        
class BodegaAdminForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'
        widgets = {
            'empresa': forms.Select(attrs={'style': correction}),
        }

class AbastecimientoRollizoAdminForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'
        widgets = {
            'rollizo': forms.Select(attrs={'style': correction}),
            'periodo': forms.Select(attrs={'style': correction,}),
        }

class CostoRollizoAdminForm(forms.ModelForm):
    class Meta:
        model = CostoRollizo
        fields = '__all__'
        widgets = {
            'linea': forms.Select(attrs={'style': correction}),
            'empresa': forms.Select(attrs={'style': correction}),
        }

class DetallePedidoAdminForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'
        widgets = {
            'pedido': forms.Select(attrs={'style': correction}),
            'producto': forms.Select(attrs={'style': correction}),
        }

class LineaHhDisponibleAdminForm(forms.ModelForm):
    class Meta:
        model = LineaHhDisponible
        fields = '__all__'
        widgets = {
            'linea': forms.Select(attrs={'style': correction}),
            'empresa': forms.Select(attrs={'style': correction}),
        }

class PedidoAdminForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            'empresa': forms.Select(attrs={'style': correction}),
        }

class PeriodoAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'tipo_periodo': forms.Select(attrs={'style': correction}),
        }

class ProductoAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'tipo_calidad': forms.Select(attrs={'style': correction}),
        }

class ProductoCorteAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'producto': forms.Select(attrs={'style': correction}),
            'patron': forms.Select(attrs={'style': correction}),
            'rollizo': forms.Select(attrs={'style': correction}),
        }

class ProductosEmpresaAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'producto': forms.Select(attrs={'style': correction}),
            'empresa': forms.Select(attrs={'style': correction}),
        }

class RollizoAdminForm(forms.ModelForm):
    class Meta:
        model = Rollizo
        fields = '__all__'
        widgets = {
            'linea': forms.Select(attrs={'style': correction}),
            'rollizo_largo': forms.Select(attrs={'style': correction}),
        }

class StockProductoAdminForm(forms.ModelForm):
    class Meta:
        model = StockProducto
        fields = '__all__'
        widgets = {
            'bodega': forms.Select(attrs={'style': correction}),
            'producto': forms.Select(attrs={'style': correction}),
        }

class TipoPeriodoAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'empresa': forms.Select(attrs={'style': correction}),
        }

class TiempoCambioAdminForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'linea': forms.Select(attrs={'style': correction}),
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

class AbastecimientoRollizoAdmin(admin.ModelAdmin):
    # cambio de apariencia
    form = AbastecimientoRollizoAdminForm
    # guarda el usuario que crea la instancia
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    # muestra tales columnas de la BD 
    list_display = ('id', 'numero_bloque', 'cantidad_hh')
    # se filtra por empresa
    list_filter = ('periodo__tipo_periodo__empresa__nombre_empresa',)
    # usuario que crea no puede ser modificado
    readonly_fields = ('usuario_crea',)

class BodegaAdmin(admin.ModelAdmin):
    # guarda usuario logueado
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

    # cambios en diseño
    form = BodegaAdminForm
    # muestra tales columnas de BD
    list_display = ('nombre_bodega', 'descripcion_bodega')
    # se ordena por id
    ordering = ('id',)
    # usuario que crea no puede ser cambiado
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['usuario_crea']
        else:
            return ['usuario_crea', 'empresa']
    # filtración por empresa
    list_filter = ('empresa__nombre_empresa',)

class CalidadProductoAdmin(admin.ModelAdmin):
    # se guarda usuario logueado
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    # usuario que crea no puede ser cambiado
    readonly_fields = ('usuario_crea',)
    # filtración por empresa
    list_filter = ('producto__productosempresa__empresa__nombre_empresa',)


class ClienteEmpresaAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        if not request.user.is_superuser:
            obj.empresa_oferente = request.user.empresa
        obj.save()
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['usuario_crea']
        else:
            return ['usuario_crea', 'empresa_oferente']
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'empresa_cliente':
            # Obtener la empresa del usuario actual
            empresa_actual = request.user.empresa
            
            # Obtener todas las empresas que aparecen en la búsqueda de ClienteEmpresa
            empresas_con_relacion = ClienteEmpresa.objects.filter(empresa_oferente=empresa_actual).values_list('empresa_cliente__rut_empresa', flat=True)
            
            # Crear un queryset que excluya la empresa del usuario actual y las empresas que aparecen en la búsqueda de ClienteEmpresa
            queryset = Empresa.objects.exclude(rut_empresa=empresa_actual.rut_empresa).exclude(rut_empresa__in=empresas_con_relacion)
            
            # Actualizar el queryset de la llave foránea empresa_cliente
            kwargs['queryset'] = queryset
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(empresa_oferente=request.user.empresa)


class CostoRollizoAdmin(admin.ModelAdmin):
    # cambios en diseño
    form = CostoRollizoAdminForm
    # se guarda usuario logueado
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('nombre_costo', 'valor_m3')
    ordering = ('nombre_costo',)
    # no se puede cambiar usuario que crea
    readonly_fields = ('usuario_crea',)
    # se filtra por empresa
    list_filter = ('empresa__nombre_empresa',)

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
            'fields': ('username', 'rut', 'empresa', 'password1', 'password2', ),
        }),
    )
    #form = UserProfileChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'rut', 'empresa')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    change_password_form = AdminPasswordChangeForm

class EmpresaAdmin(admin.ModelAdmin):
    #Modelo administrador para empresa
    def has_permission(self, request):
        # Verificar si el usuario es un superusuario
        return request.user.is_superuser
    form = EmpresaForm
    inlines = (ProductoInline,)
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('__str__', 'rut_empresa')
    ordering = ('nombre_empresa',)
    readonly_fields = ('usuario_crea',)
    list_filter = (EstadoEmpresaFilter,)

class InvInicialRollizoAdmin(admin.ModelAdmin):
    readonly_fields = ('usuario_crea',)
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

class LineaAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('nombre_linea', 'descripcion_linea')
    ordering = ('nombre_linea',)
    readonly_fields = ('usuario_crea',)
    list_filter = ('lineahhdisponible__empresa__nombre_empresa',)

class LineaHhDisponibleAdmin(admin.ModelAdmin):
    form = LineaHhDisponibleAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('id', 'numero_bloque')
    readonly_fields = ('usuario_crea',)
    list_filter = ('empresa__nombre_empresa',)

class PatronCorteAdmin(admin.ModelAdmin):
    #Modelo administrador para pedido
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('nombre_patron', 'descripcion_patron')
    ordering = ('id',)
    readonly_fields = ('usuario_crea',)
    list_filter = ('productocorte__producto__productosempresa__empresa__nombre_empresa',)

class PedidoAdmin(admin.ModelAdmin):
    #Modelo administrador para pedido
    form = PedidoAdminForm
    inlines = (DetalleProductoInline,)
    list_display = ('numero_pedido', 'prioridad', 'cliente_empresa')
    ordering = ('id',)
    readonly_fields = ('usuario_crea',)

    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            # Superusuarios pueden ver todos los pedidos
            return queryset
        else:
            # Obtener la empresa del usuario actual
            empresa = request.user.empresa
            # Filtrar los pedidos por la empresa del usuario actual
            return queryset.filter(Q(cliente_empresa__empresa_oferente=empresa) | Q(cliente_empresa__empresa_cliente=empresa))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "cliente_empresa":
            # Filtrar las opciones por la empresa del usuario actual
            kwargs["queryset"] = ClienteEmpresa.objects.filter(empresa_oferente=request.user.empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PeriodoAdmin(admin.ModelAdmin):
    form = PeriodoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('nombre_periodo', 'descripcion_periodo', 'cantidad_periodos')
    readonly_fields = ('usuario_crea',)
    list_filter = ('tipo_periodo__empresa__nombre_empresa',)

class ProductoAdmin(admin.ModelAdmin):
    #Modelo administrador para producto
    form = ProductoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('nombre_producto', 'descripcion_producto')
    ordering = ('id',)
    readonly_fields = ('usuario_crea',)
    list_filter = ('productosempresa__empresa__nombre_empresa',)

class ProductoCorteAdmin(admin.ModelAdmin):
    form = ProductoCorteAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('cantidad_producto', 'descripcion_corte')
    readonly_fields = ('usuario_crea',)
    list_filter = ('producto__productosempresa__empresa__nombre_empresa',)

class ProductosEmpresaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'producto')
    form = ProductosEmpresaAdminForm
    list_filter = ('empresa__nombre_empresa', 'producto__nombre_producto')

class RollizoAdmin(admin.ModelAdmin):
    form = RollizoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('nombre_rollizo', 'descripcion_rollizo', 'linea')
    readonly_fields = ('usuario_crea',)
    list_filter = ('linea__lineahhdisponible__empresa__nombre_empresa','linea__nombre_linea')

class RollizoLargoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('nombre_largo', 'descripcion_largo')
    readonly_fields = ('usuario_crea',)
    list_filter = ('rollizo__linea__lineahhdisponible__empresa__nombre_empresa',)

class StockProductoAdmin(admin.ModelAdmin):
    form = StockProductoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('producto', 'cantidad_m3', 'bodega')
    readonly_fields = ('usuario_crea',)
    list_filter = ('bodega__empresa__nombre_empresa', 'bodega__nombre_bodega')

class StockRollizoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('rollizo', 'cantidad', 'bodega')
    readonly_fields = ('usuario_crea',)
    list_filter = ('bodega__empresa__nombre_empresa', 'bodega__nombre_bodega')

class TiempoCambioAdmin(admin.ModelAdmin):
    form = TiempoCambioAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    readonly_fields = ('usuario_crea',)
    list_filter = ('costosobretiempo__empresa__nombre_empresa',)

class TipoPeriodoAdmin(admin.ModelAdmin):
    form = TipoPeriodoAdminForm
    def save_model(self, request, obj, form, change):
        obj.usuario_crea = request.user.rut
        obj.save()
    list_display = ('__str__',)
    readonly_fields = ('usuario_crea',)
    list_filter = ('empresa__nombre_empresa',)


admin.site.register(AbastecimientoRollizo, AbastecimientoRollizoAdmin)
admin.site.register(Bodega, BodegaAdmin)
admin.site.register(CalidadProducto, CalidadProductoAdmin)
admin.site.register(ClienteEmpresa, ClienteEmpresaAdmin)
admin.site.register(CostoRollizo, CostoRollizoAdmin)
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
