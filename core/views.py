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
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView
from django.http import JsonResponse, FileResponse, Http404
from asignaciones.models import UserProfile
from .forms import CustomUserCreationForm, LoginForm, ActualizarMateriaPrimaForm, CrearProductoForm, ProductoTerminadoForm, CrearPatronCorteForm, ActualizarPedidoForm
from .modelos.patron_corte import PatronCorte
from .modelos.producto import Producto
from .modelos.pedidos import Pedido
from .modelos.empresa import Empresa
from .modelos.materia_prima import MateriaPrima
from .modelos.productos_terminados import ProductoTerminado
from .pedidoForm import PedidoForm, DetallePedidoForm, DetallePedidoFormSet
from .queries import sel_cliente_admin, sel_pedido_empresa, sel_empresa_like, sel_pedido_productos_empresa, insertar_pedido, insertar_detalle_pedido, sel_rollizo_clasificado_empresa, sel_rollizo_empresa, sel_bodega_empresa, sel_linea_empresa, sel_producto_empresa, cantidad_pedidos_por_mes
import pyodbc, json, os, datetime, openpyxl, bleach
from django.http import JsonResponse
from datetime import datetime
import random



from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


try:
    #se conecta
    conexion = pyodbc.connect(os.environ.get('CONEXION_BD'))
    print("Conexión a base de datos exitosa")

except Exception as ex:
    print(ex)

#Hay 2 tipos de vistas, clases y funciones esta es de clases
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
    
    def post(self, request):
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
        if 'editar' in request.POST:
            pass
        elif 'eliminar' in request.POST:
            pass
        elif 'crear' in request.POST:
            form = CrearPatronCorteForm(request.POST)
            if form.is_valid():
                nuevo_patron_corte = form.save()
                return redirect('plan_patrones_corte')
    
    context = {
        'form': form,
        'patrones_corte': patrones_corte
    }
    return render(request, 'planificador/planificador_patrones_corte.html', context)

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
    
    colores = ['#4287f5', '#c1409b', '#0b9971', '#d26a52', '#0b9851', '#c4632b', '#0b4282', '#ff6600']
    
    tasks = []
    for pedido in pedidos:
        color = random.choice(colores)
        porcentaje_progreso = random.randint(10, 100)
        task_data = [
            pedido.codigo,                       
            fecha_actual,                     
            pedido.fecha_entrega.strftime('%Y/%m/%d'),
            color,                           
            porcentaje_progreso,
            pedido.nombre,   
            pedido.linea_produccion,       
            pedido.cantidad,
            pedido.cliente,
            pedido.comentario,
            pedido.producto,
            pedido.prioridad,
        ]
        tasks.append(task_data)

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

def generar_pdf_view(request):
    informacion = "Aquí va la información desde la ventana emergente."

    # Crear el objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informacion.pdf"'

    # Crear el PDF con reportlab
    buffer = canvas.Canvas(response, pagesize=letter)

    # Agregar texto al PDF
    buffer.drawString(100, 800, "Información desde la ventana emergente:")
    buffer.drawString(100, 780, informacion)

    # Guardar el PDF
    buffer.save()

    return response