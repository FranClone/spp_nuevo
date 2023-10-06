"""Este módulo mapea las URLs a las vistas (views) en la aplicación Django. Define un set de patrones que se matchean con 
las urls entrantes y las mapea hacia su vista específica. El propósito de este módulo es permitir mapear las 
URLs a la vistas que deberían manejar esas URLs. Debe trabajar en conjunto con views.py para manejar las 
solicitudes HTTP y determinar que hacer con esas request (solicitudes).
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import Administracion, Bar_chart, Carga_sv, Lista_pedidos, Login, Logout, Mantenedor, Pedidos, Register, DownloadExcel
from .views import ProductosTerminados, Dashboard 
from .views import producto, materia_prima, patron_corte, pedidos, eliminar_materia_prima, gantt_view, pantalla_carga
from .views import eliminar_patron, eliminar_producto,eliminar_producto_terminado, eliminar_pedido ,patron_editar
from .views import eliminar_patron, eliminar_producto,eliminar_producto_terminado, eliminar_pedido, materia_editar
from . import views

from .views import execute_code, eliminar_patron, eliminar_producto,eliminar_producto_terminado, eliminar_pedido,producto_editar,pedido_editar, obtener_ids_pedidos,importar, descargar_excel, linea, rollizo,eliminar_rollizo,eliminar_linea,cliente,empresa,eliminar_cliente,eliminar_empresa,linea_editar,rollizo_editar,cliente_editar,empresa_editar

from django.urls import path

urlpatterns = [
    path('administracion/', Administracion.as_view(), name = "administracion"),
    path('bar_chart/', Bar_chart.as_view(), name="bar_chart"),
    path('carga_servidor/', Carga_sv.as_view(), name = "carga_servidor"),
    path('download/', DownloadExcel.as_view(), name = "download_file"),
    path('home/', gantt_view, name = "home"),
    path('', Login.as_view(), name = "login"),
    path('lista_pedidos/', Lista_pedidos.as_view(), name = "lista_pedidos"),
    path('login/', Login.as_view(), name = "login"),
    path('logout/',Logout.as_view(), name = "logout"),
    path('mantenedor/', Mantenedor.as_view(), name = "mantenedor"),
    path('pedidos/', pedidos, name = "pedidos"),
    path('pantalla-carga/', pantalla_carga, name = "pantalla-carga"),
    path('pedidos/eliminarpedido/<int:id>', eliminar_pedido, name = "eliminar_pedido"),
    path('register/',Register.as_view(), name="register"),
    # path('asignar_folio_pedido/', asignar_folio_pedido, name = "asignar_folio_pedido"),

    # urls del menu desplegable del navbar
    path('planificador_productos_terminados/', ProductosTerminados.as_view(), name = "plan_productos_terminados"),
    path('plan_materia_prima/', materia_prima, name = "plan_materia_prima"),
    path('planificador_patrones_corte/', patron_corte, name = "plan_patrones_corte"),
    path('planificador_productos/', producto, name = "plan_productos"),
    path('plan_materia_prima/eliminarmateria/<int:id>', eliminar_materia_prima,name='eliminar_materia' ),
    path('planificador_patrones_corte/eliminarpatron/<int:id>', eliminar_patron,name='eliminar_patron' ),
    path('planificador_productos/eliminarproducto/<int:id>', eliminar_producto,name='eliminar_producto' ),
    path('planificador_productos_terminados/eliminarproducto_terminado/<int:id>', eliminar_producto_terminado,name='eliminar_producto' ),
    path('planificador_patrones_corte/editarpatroncorte/<int:id>', patron_editar, name = "patron_editar"),
    path('plan_materia_prima/editarmateria/<int:id>', materia_editar, name = "materia_editar"),
    path('obtener-ids-pedidos/',obtener_ids_pedidos, name='obtener_ids_pedidos'),
    path('planificador_productos/editarproducto/<int:id>', producto_editar, name = "producto_editar"),
    path('pedidos/editarpedido/<int:id>', pedido_editar, name = "pedido_editar"),
    path('importar/', importar, name = "importar"),
    # url para desplegar el bar chart vertical
    path('dashboard/', Dashboard.as_view(), name = "dashboard"),
    path('descargar-excel/<str:nombre_archivo>/', descargar_excel, name='descargar_excel'),
    path('planificador_linea/',linea, name = "plan_linea"),
    path('planificador_linea/editarlinea/<int:id>', linea_editar, name = "linea_editar"),
    path('planificador_linea/eliminarlinea/<int:id>',eliminar_linea, name = "eliminar_linea"),
    path('planificador_rollizo/',rollizo, name = "plan_rollizo"),
    path('planificador_rollizo/editarrollizo/<int:id>', rollizo_editar, name = "rollizo_editar"),
    path('planificador_rollizo/eliminarpatron/<int:id>',eliminar_rollizo, name = "eliminar_rollizo"),
    path('admin_cliente/',cliente, name = "admin_cliente"),
    path('admin_cliente/eliminarcliente/<int:id>',eliminar_cliente, name = "eliminar_cliente"),
    path('admin_cliente/admin_clienteeditar/<int:id>',cliente_editar, name = "cliente_editar"),
    path('admin_empresa/',empresa, name = "admin_empresa"),
    path('admin_empresa/eliminarempresa/<int:id>',eliminar_empresa, name = "eliminar_empresa"),
    path('admin_empresa/admin_empresaeditar/<int:id>',empresa_editar, name = "empresa_editar"),
    path('execute_code/<str:archivo1>/<str:archivo2>/', views.execute_code, name='execute_code'),  



    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
