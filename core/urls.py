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
from .views import execute_code, eliminar_patron, eliminar_producto,eliminar_producto_terminado, eliminar_pedido,producto_editar,pedido_editar, obtener_ids_pedidos,importar, descargar_excel, linea, rollizo,eliminar_rollizo,eliminar_linea,cliente,empresa,eliminar_cliente,eliminar_empresa
from django.urls import path
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('administracion/', login_required(Administracion.as_view()), name="administracion"),
    path('bar_chart/', login_required(Bar_chart.as_view()), name="bar_chart"),
    path('carga_servidor/', login_required(Carga_sv.as_view()), name="carga_servidor"),
    path('download/', login_required(DownloadExcel.as_view()), name="download_file"),
    path('home/', login_required(gantt_view), name="home"),
    path('', Login.as_view(), name="login"),
    path('lista_pedidos/', login_required(Lista_pedidos.as_view()), name="lista_pedidos"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('mantenedor/', login_required(Mantenedor.as_view()), name="mantenedor"),
    path('pedidos/', login_required(pedidos), name="pedidos"),
    path('pantalla-carga/', login_required(pantalla_carga), name="pantalla-carga"),
    path('pedidos/eliminarpedido/<int:id>', login_required(eliminar_pedido), name="eliminar_pedido"),
    path('register/', Register.as_view(), name="register"),
    # path('asignar_folio_pedido/', asignar_folio_pedido, name = "asignar_folio_pedido"),

    # urls del menu desplegable del navbar
    path('planificador_productos_terminados/', login_required(ProductosTerminados.as_view()), name="plan_productos_terminados"),
    path('plan_materia_prima/', login_required(materia_prima), name="plan_materia_prima"),
    path('planificador_patrones_corte/', login_required(patron_corte), name="plan_patrones_corte"),
    path('planificador_productos/', login_required(producto), name="plan_productos"),
    path('plan_materia_prima/eliminarmateria/<int:id>', login_required(eliminar_materia_prima), name='eliminar_materia'),
    path('planificador_patrones_corte/eliminarpatron/<int:id>', login_required(eliminar_patron), name='eliminar_patron'),
    path('planificador_productos/eliminarproducto/<int:id>', login_required(eliminar_producto), name='eliminar_producto'),
    path('planificador_productos_terminados/eliminarproducto_terminado/<int:id>', login_required(eliminar_producto_terminado), name='eliminar_producto_terminado'),
    path('planificador_patrones_corte/editarpatroncorte/<int:id>', login_required(patron_editar), name="patron_editar"),
    path('plan_materia_prima/editarmateria/<int:id>', login_required(materia_editar), name="materia_editar"),
    path('obtener-ids-pedidos/', login_required(obtener_ids_pedidos), name='obtener_ids_pedidos'),
    path('planificador_productos/editarproducto/<int:id>', login_required(producto_editar), name="producto_editar"),
    path('pedidos/editarpedido/<int:id>', login_required(pedido_editar), name="pedido_editar"),
    path('importar/', login_required(importar), name="importar"),
    # url para desplegar el bar chart vertical
    path('dashboard/', login_required(Dashboard.as_view()), name="dashboard"),
    path('descargar-excel/<str:nombre_archivo>/', login_required(descargar_excel), name='descargar_excel'),
    path('planificador_linea/', login_required(linea), name="plan_linea"),
    path('planificador_linea/eliminarlinea/<int:id>', login_required(eliminar_linea), name="eliminar_linea"),
    path('planificador_rollizo/', login_required(rollizo), name="plan_rollizo"),
    path('planificador_rollizo/eliminarpatron/<int:id>', login_required(eliminar_rollizo), name="eliminar_rollizo"),
    path('admin_cliente/', login_required(cliente), name="admin_cliente"),
    path('admin_cliente/eliminarcliente/<int:id>', login_required(eliminar_cliente), name="eliminar_cliente"),
    path('admin_empresa/', login_required(empresa), name="admin_empresa"),
    path('admin_cliente/eliminarempresa/<int:id>', login_required(eliminar_empresa), name="eliminar_empresa"),
    path('execute_code/<str:archivo1>/<str:archivo2>/', login_required(views.execute_code), name='execute_code'),



    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
