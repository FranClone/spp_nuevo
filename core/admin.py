from admin_interface.models import Theme
from django.contrib import admin
from .modelos.bodega import Bodega
from .modelos.empresa import Empresa
from .modelos.linea import Linea
from .modelos.pedido import Pedido
from .modelos.producto import Producto
from .modelos.detalle_pedido import DetallePedido
from .models import UserProfile

#EN PROCESO DE TOTAL CAMBIO

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
    list_display = ('get_username', 'rut_empresa')
    ordering = ('user__id',)
    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'

class BodegaAdmin(admin.ModelAdmin):
    list_display = ('nombre_bodega', 'descripcion_bodega')
    ordering = ('id_bodega',)
    list_filter = ('rut_empresa__nombre_empresa',)

class EmpresaAdmin(admin.ModelAdmin):
    #Modelo administrador para empresa
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
    list_display = ('detalle_producto','volumen_producto')
    ordering = ('id_pedido',)
    list_filter = ('id_pedido__rut_empresa__nombre_empresa','id_pedido__numero_pedido', 'id_producto__nombre_producto')

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