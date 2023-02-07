"""Este módulo mapea las URLs a las vistas (views) en la aplicación Django. Define un set de patrones que se matchean con 
las urls entrantes y las mapea hacia su vista específica. El propósito de este módulo es permitir mapear las 
URLs a la vistas que deberían manejar esas URLs. Debe trabajar en conjunto con views.py para manejar las 
solicitudes HTTP y determinar que hacer con esas request (solicitudes).
"""
from django.contrib import admin
from django.urls import path
from .views import Administracion, Bar_chart, Carga_sv, Home, Index, Inventario_pdto, Inventario_roll, Inventario_roll_nc, Lista_pedidos, Login, logout, Mantenedor, Productos, Register
from .views import Plan_Bodega, Plan_Lineas, Plan_Productos, Plan_Rollizo
from .views import get_data

# urlpatterns lista las rutas de las URLs a las views
urlpatterns = [
    path('administracion/', Administracion.as_view(), name = "administracion"),
    path('bar_chart/', Bar_chart.as_view(), name="bar_chart"),
    path('carga_servidor/', Carga_sv.as_view(), name = "carga_servidor"),
    path('home/', Home.as_view(), name = "home"),
    path('', Index.as_view(), name = "index"),
    path('inventario_producto/', Inventario_pdto.as_view(), name = "inventario_producto"),
    path('inventario_rollizo/', Inventario_roll.as_view(), name = "inventario_rollizo"),
    path('inventario_rollizo_nc/', Inventario_roll_nc.as_view(), name = "inventario_rollizo_nc"),
    path('lista_pedidos/', Lista_pedidos.as_view(), name = "lista_pedidos"),
    path('login/', Login.as_view(), name = "login"),
    path('logout/',logout, name = "logout"),
    path('mantenedor/', Mantenedor.as_view(), name = "mantenedor"),
    path('productos/', Productos.as_view(), name = "productos"),
    path('register/',Register.as_view(), name="register"),
    # urls del menu desplegable del navbar
    path('planificador_bodega/', Plan_Bodega.as_view(), name = "plan_bodega"),
    path('planificador_lineas/', Plan_Lineas.as_view(), name = "plan_lineas"),
    path('planificador_productos/', Plan_Productos.as_view(), name = "plan_productos"),
    path('planificador_rollizo/', Plan_Rollizo.as_view(), name = "plan_rollizo"),
    # url para desplegar el bar chart vertical
    path('get-data/', get_data, name='get-data')
]
