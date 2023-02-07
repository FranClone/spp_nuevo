"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import Administracion, Bar_chart, Carga_sv, Home, Index, Inventario_pdto, Inventario_roll, Inventario_roll_nc, Lista_pedidos, Login, Logout, Mantenedor, Productos, Register
from .views import Plan_Bodega, Plan_Lineas, Plan_Productos, Plan_Rollizo

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
    path('logout/',Logout.as_view(), name = "logout"),
    path('mantenedor/', Mantenedor.as_view(), name = "mantenedor"),
    path('productos/', Productos.as_view(), name = "productos"),
    path('register/',Register.as_view(), name="register"),
    #urls menu desplegable de header, planificador
    path('planificador_bodega/', Plan_Bodega.as_view(), name = "plan_bodega"),
    path('planificador_lineas/', Plan_Lineas.as_view(), name = "plan_lineas"),
    path('planificador_productos/', Plan_Productos.as_view(), name = "plan_productos"),
    path('planificador_rollizo/', Plan_Rollizo.as_view(), name = "plan_rollizo"),
]
