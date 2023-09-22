"""En este módulo se definen todas las vistas para la aplicación web y la lógica para las solicitudes HTTP. 
Maneja las request del usuario y responde con contenido como páginas HTML, JSON, entre otros.
En Django, una vista es una función de Python o basada en clases que toma una web request y devuelve una web response.
Las vistas están típicamente asociadas con una URL en el módulo 'urls.py'.
"""
from django.conf import settings
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView
from django.http import JsonResponse, FileResponse, Http404
#from asignaciones.models import UserProfile
from .forms import CustomUserCreationForm, LoginForm, ActualizarMateriaPrimaForm, CrearProductoForm, ProductoTerminadoForm ,CrearPatronCorteForm, ActualizarPedidoForm
from .modelos.patron_corte import PatronCorte
from .modelos.producto import Producto
from .modelos.pedidos import Pedido
from .modelos.cliente import Cliente
from .modelos.empresa import Empresa
from .modelos.materia_prima import MateriaPrima
from .modelos.productos_terminados import ProductoTerminado
from .modelos.cliente import Cliente
from .modelos.resources import PedidoResource
from .pedidoForm import PedidoForm, DetallePedidoForm, DetallePedidoFormSet
from .queries import sel_cliente_admin, sel_pedido_empresa, sel_empresa_like, sel_pedido_productos_empresa, insertar_pedido, insertar_detalle_pedido, sel_rollizo_clasificado_empresa, sel_rollizo_empresa, sel_bodega_empresa, sel_linea_empresa, sel_producto_empresa, cantidad_pedidos_por_mes
import pyodbc, json, os, datetime, openpyxl, bleach
from django.http import JsonResponse
from datetime import datetime
import random
from django.urls import reverse
import pandas as pd
from django.db import connection
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tablib import Dataset 
from .forms import Excelform
from django.contrib import messages
import logging  # Import the logging module
try:
    #se conecta
    conexion = pyodbc.connect(os.environ.get('CONEXION_BD'))
    print("Conexión a base de datos exitosa")

except Exception as ex:
    print(ex)



from django.shortcuts import render
from mip import Model, xsum, maximize, BINARY, CBC
#Test Algoritmo
def mochila(request):

    p = [10, 13, 18, 31, 7, 15]
    w = [11, 15, 20, 35, 10, 33]
    c, I = 47, range(len(w))
    m = Model('mochila',maximize,CBC)

    x = [m.add_var(var_type=BINARY) for i in I]
    m.objective = maximize(xsum(p[i] * x[i] for i in I))
    m += xsum(w[i] * x[i] for i in I) <= c
    m.optimize()
    selected = [i for i in I if x[i].x >= 0.99]
    #
    selected_profits = [p[i] for i in selected]
    selected_weights = [w[i] for i in selected]
    print("selected items: {}".format(selected))

    return render(request, 'mochila.html', {'selected': selected,'selected_profits':selected_profits,'selected_weights':selected_weights})




def importar(request):
    if request.method == 'POST':
        print("post")
        if 'subir' in request.POST:
            result = process_uploaded_file(request.FILES.get('xlsfile'))
            if result.get('success'):
                # Log success message to the console
                print("File uploaded and processed successfully.")
            else:
                # Log error message to the console
                print("Data import failed. Please check the file format.")
        
    #return render(request, 'home.html')
    return redirect(reverse('home')) 


def process_uploaded_file(xlsfile):
    if xlsfile:
        try:
            # Cargar el archivo Excel en un DataFrame de pandas
            df = pd.read_excel(xlsfile)

            with transaction.atomic():
                # Use a transaction to ensure data integrity

                # Crear una instancia de Pedido para cada registro y guardarla en la base de datos
                for index, row in df.iterrows():
                    productos_str = str(row['producto'])  # Convert 'producto' to a string
                    if productos_str and isinstance(productos_str, str):
                        productos_list = [producto.strip() for producto in productos_str.split(',')]  # Split and clean product names
                        
                        id_cliente = row['cliente']
                        try:
                            cliente = Cliente.objects.get(id=id_cliente)
                        except Cliente.DoesNotExist:
                            print(f"Cliente con id {id_cliente} no existe.")
                            continue

                        pedido = Pedido(
                            cliente=cliente,
                            fecha_produccion=row['fecha_produccion'],
                            fecha_entrega=row['fecha_entrega'],
                            orden_pedido=row['orden_pedido'],
                            comentario=row['comentario'],
                            prioridad=row['prioridad'],
                            version=row['version'],
                            estado=row['estado']
                        )
                        pedido.save()

                        # Asignar los productos usando the method .set()
                        productos = Producto.objects.filter(nombre__in=productos_list)
                        pedido.producto.set(productos)

                print("Importación exitosa.")

        except Exception as e:
            print(f"Fallo en la importación de datos: {str(e)}")

    return {'success': True}


class Administracion(View):
    @method_decorator(login_required) #HomeView da acceso a ambos, get req y post req. Get request pide la info para tu ver, post request es lo que envias para que el servidor haga algo con esa información
    def get(self, request, *args, **kwargs):
        rut_empresa = request.user.empresa.rut_empresa
        rows = sel_cliente_admin(rut_empresa)
        return render(request, 'administracion.html', {"rows":rows}) 

class Bar_chart(View):
    @method_decorator(login_required) #HomeView da acceso a ambos, get req y post req. Get request pide la info para tu ver, post request es lo que envias para que el servidor haga algo con esa información
    def get(self, request, *args, **kwargs):
        """Esta clase define la vista del bar chart"""
        # calculo pedidos, estos deben venir de la base de datos
        mcubicos_pedido_producto = [4000, 5000, 6000, 7000, 8000, 7000]
        mcubicos_cortados_producto = [2000, 3000, 2500, 2000, 4000, 7000]
        produccion_global = []
        
        # se realiza el cálculo matemático para obtener los valores porcentuales de cada pedido
        for i in range(len(mcubicos_pedido_producto)):
            produccion_global.append((mcubicos_cortados_producto[i] / mcubicos_pedido_producto[i]) * 100)
            
        return render(request, 'bar_chart.html', {"pr_global":json.dumps(produccion_global)})

class Carga_sv(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        rut_empresa = request.user.empresa.rut_empresa
        rows = sel_pedido_empresa(rut_empresa)
        prioridades = ['Alta', 'Media', 'Baja']
        return render(request, 'carga_servidor.html', {"rows":rows, "prioridades":prioridades})

class DownloadExcel(View):
    # Descarga plantilla excel para llenar pedidos
    def get(self, request, *args, **kwargs):
        file_name = "Formato Ejemplo.xlsx"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['content_type'] = 'application/vnd.ms-excel'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
            return response
        raise Http404
    
def get_empresas(request):
    '''Esta vista es usada en el formulario de pedidos
    para que aparezca la busqueda del top 5 de empresas que correspondan al rut'''
    parte_rut = request.GET.get('parte_rut', '')
    empresas = []
    if parte_rut:
        empresas = list(sel_empresa_like(parte_rut))
    return JsonResponse({'empresas': empresas})

class Index(View): 
    """Esta clase define la vista Index"""
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'index.html', context)

class Inventario_pdto(View): 
    """Esta clase define la vista de Inventario"""
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'inventario_producto.html', context)

class Inventario_roll(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        #lista de clases diamétricas, desde 14 hasta 40
        clase_diametrica = list(range(14, 41, 2))
        rut_empresa = request.user.empresa.rut_empresa
        clas = sel_rollizo_clasificado_empresa(rut_empresa)
        noclas = sel_rollizo_empresa(rut_empresa)
        return render(request, 'inventario_rollizo.html', {"clase_diametrica": clase_diametrica, "clas":clas, "noclas":noclas})

class Pedidos(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'pedidos.html') 

class Lista_pedidos(View): 
    """Esta clase define la vista de Lista de Pedidos"""
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'lista_pedidos.html', context)
    
class Login(View):
    def get(self, request):
        return render(request, 'login.html')


    #verifica si la solicitud HTTP es de tipo POST
    def post(self, request):
        
        """if request.method == 'POST':
            print(request.POST)
            #Se obtienen los valores del campo "Rut" y "contraseña" del formulario
            Rut = request.POST.get('Rut')
            contraseña = request.POST.get('contraseña')
            #autenticar al usuario utilizando el valor del campo "Rut" como nombre de usuario y el valor del campo "contraseña"
            user = authenticate(request, username=Rut, password=contraseña)
            if user:
                #Si el usuario se autentica correctamente, se inicia sesión
                print("pasop")
                login(request, user)
                # se redirige al usuario a una página
                return redirect('pantalla-carga')
            else:
                #Si la autenticación no tiene éxito, se renderiza la plantilla 'login.html' nuevamente
                print("paso aqui")
                return render(request, 'login.html', {"error": "Usuario no valido"})
        return render(request, 'login.html')"""
        return redirect('pantalla-carga')
    

class Logout(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class Mantenedor(View): 
    """Esta clase define la vista de Mantenedor"""
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'mantenedor.html', context)

class Register(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})

class ProductosTerminados(View):
    def get(self, request, *args, **kwargs):
        productos_terminados = ProductoTerminado.objects.all()
        form = ProductoTerminadoForm()
        return render(request, 'planificador/planificador_productos_terminados.html', {'productos_terminados': productos_terminados, 'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ProductoTerminadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plan_productos_terminados')
        
        productos_terminados = ProductoTerminado.objects.all()
        return render(request, 'planificador/planificador_productos_terminados.html', {'productos_terminados': productos_terminados, 'form': form})

class Plan_Patrones_Corte(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'planificador/planificador_patrones_corte.html')

class Plan_Productos(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'planificador/planificador_productos.html')

class Dashboard(View): 
    """Esta clase define la vista Dashboard"""
    def get(self, request, *args, **kwargs):
        
        return render(request, 'dashboard.html')

def materia_prima(request):
    materias_primas = MateriaPrima.objects.all()

    if request.method == 'POST':
        if 'editar' in request.POST:
            pass
        elif 'eliminar' in request.POST:
            pass
        elif 'crear' in request.POST:
            form = ActualizarMateriaPrimaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('plan_materia_prima')

    else:
        form = ActualizarMateriaPrimaForm()

    context = {
        'form': form,
        'materias_primas': materias_primas
    }
    return render(request, 'planificador/planificador_materia_prima.html', context)

def producto(request):
    productos = Producto.objects.all()
    form = CrearProductoForm()

    if request.method == 'POST':
        if 'editar' in request.POST:
            pass
        elif 'eliminar' in request.POST:
            pass
        elif 'crear' in request.POST:
            form = CrearProductoForm(request.POST)
            if form.is_valid():
                print("Formulario válido")  # Mensaje de depuración
                nuevo_producto = form.save()
                print("Producto guardado en la base de datos con ID:", nuevo_producto.id)  # Mensaje de depuración
                return redirect('plan_productos')
            else:
                print("Formulario inválido")  # Mensaje de depuración
        else:
            print("Acción no reconocida")  # Mensaje de depuración

    context = {
        'form': form,
        'productos': productos
    }
    return render(request, 'planificador/planificador_productos.html', context)


def patron_corte(request):
    patrones_corte = PatronCorte.objects.all()
    form = CrearPatronCorteForm()

    if request.method == 'POST':
        if 'crear' in request.POST:
            form = CrearPatronCorteForm(request.POST)
            if form.is_valid():
                nuevo_patron_corte = form.save()
                return redirect('plan_patrones_corte')
    
    context = {
        'form': form,
        'patrones_corte': patrones_corte
    }
    return render(request, 'planificador/planificador_patrones_corte.html', context)


def patron_editar(request,id):
    patron= PatronCorte.objects.get(id=id)
    data = {'form': CrearPatronCorteForm(instance=patron),'id':id}
    if request.method == 'POST':
        formulario = CrearPatronCorteForm(data = request.POST, instance=patron)
        if formulario.is_valid():
            formulario.save()
            return redirect('plan_patrones_corte')
        else:
            print("errorr")
    return render(request, 'planificador/planificador_patronescorteeditar.html', data)


def pantalla_carga(request):
    return render(request, 'pantalla-carga.html')

def pedidos(request):
    pedidos = Pedido.objects.all()

    if request.method == 'POST':
        if 'editar' in request.POST:
            pass
        elif 'eliminar' in request.POST:
            pass
        elif 'crear' in request.POST:
            form = ActualizarPedidoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('pedidos')

    else:
        form = ActualizarPedidoForm()

    context = {
        'form': form,
        'pedidos': pedidos
    }
    return render(request, 'pedidos.html', context)

def gantt_view(request):
    
    form = ActualizarPedidoForm() 
    pedidos = Pedido.objects.all()

    fecha_actual = datetime.today().strftime('%Y/%m/%d')
    
    prioridad_colores = {
    'alto': '#ff0000',  # Rojo para alta prioridad
    'mediano': '#E3DA4D',  # Naranja para media prioridad
    'bajo': '#0b9851',  # Verde para baja prioridad
    'Alto': '#ff0000',
    'Medio': '#E3DA4D',
    'Bajo': '#0b9851',
    'Alta': '#ff0000',
    'Media': '#E3DA4D',
    'Baja': '#0b9851',
    'alta': '#ff0000',
    'media': '#E3DA4D',
    'baja': '#0b9851'
}
    
    colores = ['#4287f5', '#c1409b', '#0b9971', '#d26a52', '#0b9851', '#c4632b', '#0b4282', '#ff6600']

    tasks=[]
    for pedido in pedidos:

        productos = pedido.producto.all()
        
        if productos.exists():
            for producto in productos:
                productos_name = [producto.nombre]
                producto_codigo = [producto.codigo]
                porcentaje_progreso = random.randint(10, 100)
                nombre_cliente = pedido.cliente.nombre_cliente if pedido.cliente else "N/A"  # "N/A" si no hay cliente
                nombre_linea = producto.linea.nombre_linea
                color = random.choice(colores)
                color_p = prioridad_colores.get(pedido.prioridad, '#4287f5')
                tasks_pedido = [
                    pedido.orden_pedido,
                    fecha_actual,   # 1
                    pedido.fecha_entrega.strftime('%Y/%m/%d'),  # 2
                    pedido.fecha_produccion.strftime('%Y/%m/%d'),  # 3
                    porcentaje_progreso,  # 4
                    nombre_cliente,  # 5
                    pedido.comentario,  # 6
                    productos_name,  # 7
                    pedido.prioridad,  # 8
                    producto_codigo,  #9 Agregar el código del producto
                    nombre_linea, #10
                    color,  # 11
                    color_p  # 12
                ]

                tasks.append(tasks_pedido)
        else:
            # Si no hay productos asociados al pedido, se crea una entrada con valores predeterminados
            #productos_name = ["N/A"]
            #producto_codigo = ["N/A"]
            largo = [producto.largo for producto in pedido.producto.all()]
            ancho = [producto.ancho for producto in pedido.producto.all()]
            alto = [producto.alto for producto in pedido.producto.all()]
            color = random.choice(colores)
            color_p = prioridad_colores.get(pedido.prioridad, '#4287f5')
            porcentaje_progreso = random.randint(10, 100)
            nombre_cliente = pedido.cliente.nombre_cliente if pedido.cliente else "N/A"  # "N/A" si no hay cliente
            nombre_linea = producto.linea.nombre_linea
            descripcion = producto.descripcion
            inventario_inicial = producto.inventario_inicial
            valor_inventario = producto.valor_inventario
            costo_almacenamiento = producto.costo_almacenamiento
            nombre_rollizo = producto.nombre_rollizo.nombre_rollizo if producto.nombre_rollizo else "N/A"
            inventario_final = producto.inventario_final
            patron_corte = [patron.nombre_patron for patron in producto.patron_corte.all()]
            tasks_pedido = [
                pedido.orden_pedido,
                fecha_actual,   # 1
                pedido.fecha_entrega.strftime('%Y/%m/%d'),  # 2
                pedido.fecha_produccion.strftime('%Y/%m/%d'),  # 3
                porcentaje_progreso,  # 4
                nombre_cliente,  # 5
                productos_name,  # 6
                producto_codigo,  # 7
                largo, #8
                ancho, #9
                alto, #10
                color,  # 11
                color_p,  # 12
                nombre_linea,# 13
                descripcion,# 14
                inventario_inicial,# 15
                valor_inventario,# 16
                costo_almacenamiento,# 17
                nombre_rollizo,# 18
                inventario_final,# 19
                patron_corte,# 20
            ]

            tasks.append(tasks_pedido)

    return render(request, 'home.html', {'tasks': tasks, 'form': form})


def eliminar_materia_prima(request,id):
    materia_prima=MateriaPrima.objects.get(id=id)
    materia_prima.delete()

    return redirect('plan_materia_prima')

def eliminar_pedido(request,id):
    pedido=Pedido.objects.get(id=id)
    pedido.delete()

    return redirect('pedidos')

def eliminar_patron(request,id):
    patron=PatronCorte.objects.get(id=id)
    patron.delete()

    return redirect('plan_patrones_corte')

def eliminar_producto(request,id):
    producto=Producto.objects.get(id=id)
    producto.delete()

    return redirect('plan_productos')

def eliminar_producto_terminado(request,id):
    producto_terminado=ProductoTerminado.objects.get(id=id)
    producto_terminado.delete()

    return redirect('plan_productos_terminados')

def producto_editar(request,id):
    prod= Producto.objects.get(id=id)
    data = {'form': CrearProductoForm(instance=prod),'id':id}
    if request.method == 'POST':
        formulario = CrearProductoForm(data = request.POST, instance=prod)
        if formulario.is_valid():
            formulario.save()
            return redirect('plan_productos')
        else:
            print("error")
    return render(request, 'planificador/planificador_productoseditar.html', data)
    
def pedido_editar(request,id):
    prod= Pedido.objects.get(id=id)
    data = {'form': ActualizarPedidoForm(instance=prod),'id':id}
    if request.method == 'POST':
        formulario = ActualizarPedidoForm(data = request.POST, instance=prod)
        if formulario.is_valid():
            formulario.save()
            return redirect('pedidos')
        else:
            print("error")
    return render(request, 'pedidoseditar.html', data)

def materia_editar(request,id):
    prod= MateriaPrima.objects.get(id=id)
    data = {'form': ActualizarMateriaPrimaForm(instance=prod),'id':id}
    if request.method == 'POST':
        formulario = ActualizarMateriaPrimaForm(data = request.POST, instance=prod)
        if formulario.is_valid():
            formulario.save()
            return redirect('plan_materia_prima')
        else:
            print("error")
    return render(request, 'planificador/editar_materia_prima.html', data)
    
#Verificacion de nuevos pedidos para el aviso de inicio

def obtener_ids_pedidos(request):
    ids_pedidos = Pedido.objects.values_list('id', flat=True)
    return JsonResponse({'ids_pedidos': list(ids_pedidos)})

def descargar_excel(request, nombre_archivo):
    # Obtén la ruta completa del archivo Excel en la carpeta 'media'
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, nombre_archivo)
    
    if os.path.exists(ruta_archivo):
        # Abre el archivo y crea una respuesta de descarga
        with open(ruta_archivo, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            return response
    else:
        raise Http404("El archivo no existe")

