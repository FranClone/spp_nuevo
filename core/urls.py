"""Este módulo mapea las URLs a las vistas (views) en la aplicación Django. Define un set de patrones que se matchean con 
las urls entrantes y las mapea hacia su vista específica. El propósito de este módulo es permitir mapear las 
URLs a la vistas que deberían manejar esas URLs. Debe trabajar en conjunto con views.py para manejar las 
solicitudes HTTP y determinar que hacer con esas request (solicitudes).
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import Administracion, Bar_chart, Carga_sv, Home,Lista_pedidos, Login, Logout, Mantenedor, Pedidos, Register, DownloadExcel
from .views import ProductosTerminados, Plan_Patrones_Corte, Dashboard 
from .views import productos_view, materia_prima

urlpatterns = [
    path('administracion/', Administracion.as_view(), name = "administracion"),
    path('bar_chart/', Bar_chart.as_view(), name="bar_chart"),
    path('carga_servidor/', Carga_sv.as_view(), name = "carga_servidor"),
    path('download/', DownloadExcel.as_view(), name = "download_file"),
    path('home/', Home.as_view(), name = "home"),
    path('', Login.as_view(), name = "login"),
    path('pedidos/', Pedidos.as_view(), name = "pedidos"),
    path('lista_pedidos/', Lista_pedidos.as_view(), name = "lista_pedidos"),
    path('login/', Login.as_view(), name = "login"),
    path('logout/',Logout.as_view(), name = "logout"),
    path('mantenedor/', Mantenedor.as_view(), name = "mantenedor"),
    path('pedido/', Pedidos.as_view(), name = "pedido"),
    path('register/',Register.as_view(), name="register"),
    # urls del menu desplegable del navbar
    path('planificador_productos_terminados/', ProductosTerminados.as_view(), name = "plan_productos_terminados"),
    path('plan_materia_prima/', materia_prima, name = "plan_materia_prima"),
    path('planificador_patrones_corte/', Plan_Patrones_Corte.as_view(), name = "plan_patrones_corte"),
    path('planificador_productos/', productos_view, name = "plan_productos"),
    path('dashboard/', Dashboard.as_view(), name = "dashboard")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
