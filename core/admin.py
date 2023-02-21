from django.contrib import admin
from .modelos.pedido import Pedido
from .modelos.empresa import Empresa
from .modelos.producto import Producto

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('rut_empresa', 'nombre_empresa')
    ordering = ('rut_empresa',)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'descripcion_producto')
    ordering = ('id_producto',)
    list_filter = ('rut_empresa',)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero_pedido', 'prioridad')
    ordering = ('id_pedido',)
    list_filter = ('rut_empresa',)

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Pedido, PedidoAdmin)