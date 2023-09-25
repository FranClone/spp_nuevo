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

from .forms import CustomUserCreationForm, DetallePedidoForm,LoginForm, ActualizarMateriaPrimaForm, CrearProductoForm, ProductoTerminadoForm ,CrearPatronCorteForm, ActualizarPedidoForm, CrearLineaForm, CrearRollizoForm, CrearClienteForm, CrearEmpresaForm

from .modelos.patron_corte import PatronCorte
from .modelos.producto import Producto
from .modelos.pedidos import Pedido
from .modelos.rollizo import Rollizo
from .modelos.linea import Linea
from .modelos.detalle_pedido import DetallePedido
from .modelos.cliente import Cliente
from .modelos.empresa import Empresa
from .modelos.materia_prima import MateriaPrima
from .modelos.productos_terminados import ProductoTerminado
from django.forms import inlineformset_factory
from .modelos.detalle_pedido import DetallePedido
from .modelos.resources import PedidoResource
#from .pedidoForm import PedidoForm, DetallePedidoForm, DetallePedidoFormSet
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
from django.forms import formset_factory
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

                        for producto_nombre in productos_list:
                            producto = Producto.objects.get(nombre=producto_nombre)
                            detalle_pedido = DetallePedido(
                                pedido=pedido,
                                producto=producto,
                                alto_producto=row['alto'],
                                ancho_producto=row['ancho'],
                                largo_producto=row['largo'],
                                volumen_producto=row['volumen_producto'],
                                fecha_entrega=row['fecha_entrega'],
                                grado_urgencia=row['prioridad'], 
                                cantidad_piezas=row['cantidad_piezas'],
                                cantidad_trozos=row['cantidad_trozos'],
                                piezas_xpaquete=row['piezas_xpaquete'],
                                piezas_xtrozo=row['piezas_xtrozo'],
                                paquetes_solicitados=row['paquetes_solicitados'],
                                paquetes_saldo=row['paquetes_saldo'],
                                detalle_producto=row['comentario'],
                            )
                            detalle_pedido.save()
                                # Obtiene la fecha y hora actual formateada
                        fecha_actual = datetime.now()
                        fecha_actual_formateada = fecha_actual.strftime('%d-%m-%Y %H:%M')

                                # Agrega 'titulofecha' al contexto para pasarlo a la plantilla
                        titulofecha = {
                            'titulofecha': f"(Cargados {fecha_actual_formateada})"
                            }
                        
                        print(titulofecha)

                        

                        productos = Producto.objects.filter(nombre__in=productos_list)
                        pedido.producto.set(productos)
                    
                print("Importación exitosa.")
        except Exception as e:
            print(f"Error processing row {index + 2}: {str(e)}")


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

#Form pedido y detalle pedido
def pedidos(request):
    pedidos = Pedido.objects.all()
    DetallePedidoFormSet = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=1, can_delete=True)
    detalle_pedido_formset = DetallePedidoFormSet(prefix='detalle_pedido')
    if request.method == 'POST':
        if 'editar' in request.POST:
            pass
        elif 'eliminar' in request.POST:
            pass
        elif 'crear' in request.POST:
            # Handle Pedido form
            pedido_form = ActualizarPedidoForm(request.POST)
            
            if pedido_form.is_valid():
                # Save the Pedido instance
                pedido_instance = pedido_form.save()
                
                # Create a formset with the Pedido instance
                DetallePedidoFormSet = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=1, can_delete=True)
                detalle_pedido_formset = DetallePedidoFormSet(request.POST, prefix='detalle_pedido', instance=pedido_instance)
                
                if detalle_pedido_formset.is_valid():
                
                    for form in detalle_pedido_formset:
                        # Get the Producto instance from the form data
                        producto_instance   = form.cleaned_data.get('producto')
                        producto_code = producto_instance.id
                        producto_id = int(producto_code)
                        print(producto_id)
                        try:
                            producto = Producto.objects.get(id=producto_id)
                        except Producto.DoesNotExist:
                            producto = None

                        if producto is not None:
                            # Set the Producto for this DetallePedido
                            form.instance.producto = producto
                    detalle_pedido_formset.save()
                    print(f"Producto with id {producto_id} does not exist.")
                        # detalle_pedido_form.producto = producto
                        # detalle_pedido_form.save()
                    
                    print("Formset cleaned data:", detalle_pedido_formset.cleaned_data)
                    return redirect('pedidos')
                else:
                    print("Pedido Form Errors:", pedido_form.errors)
                    print("Detalle Pedido Formset Errors:")
                    for form in detalle_pedido_formset:
                        print(form.errors)
            else:
                print("Pedido Form Errors:", pedido_form.errors)
        else:
            pedido_form = ActualizarPedidoForm()
    else:
        pedido_form = ActualizarPedidoForm()

    context = {
        'pedido_form': pedido_form,
        'detalle_pedido_formset': detalle_pedido_formset,
        'pedidos': pedidos
    }

    return render(request, 'pedidos.html', context)


def gantt_view(request):
    
    pedido_form = ActualizarPedidoForm()
    DetallePedidoFormSet = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=1, can_delete=True)
    detalle_pedido_formset = DetallePedidoFormSet(prefix='detalle_pedido')

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
                largo = [producto.largo for producto in pedido.producto.all()]
                ancho = [producto.ancho for producto in pedido.producto.all()]
                alto = [producto.alto for producto in pedido.producto.all()]
                productos_name = [producto.nombre]
                producto_codigo = [producto.codigo]
                porcentaje_progreso = random.randint(10, 100)
                nombre_cliente = pedido.cliente.nombre_cliente if pedido.cliente else "N/A"  # "N/A" si no hay cliente
                nombre_linea = producto.linea.nombre_linea
                color = random.choice(colores)
                color_p = prioridad_colores.get(pedido.prioridad, '#4287f5')
                descripcion = producto.descripcion
                inventario_inicial = producto.inventario_inicial
                valor_inventario = producto.valor_inventario
                costo_almacenamiento = producto.costo_almacenamiento
                nombre_rollizo = producto.nombre_rollizo.nombre_rollizo if producto.nombre_rollizo else "N/A"
                patron_corte = [pc.nombre for pc in producto.patron_corte.all()] if producto.patron_corte.exists() else ["N/A"]
                detalle_pedido = DetallePedido.objects.get(pedido=pedido, producto=producto)
                alto_producto = detalle_pedido.alto_producto if detalle_pedido.alto_producto is not None else "N/A"
                ancho_producto = detalle_pedido.ancho_producto if detalle_pedido.ancho_producto is not None else "N/A"
                largo_producto = detalle_pedido.largo_producto if detalle_pedido.largo_producto is not None else "N/A"
                volumen_producto = detalle_pedido.volumen_producto if detalle_pedido.volumen_producto is not None else "N/A"
                estado_pedido_linea = detalle_pedido.estado_pedido_linea if detalle_pedido.estado_pedido_linea is not None else "N/A"
                grado_urgencia = detalle_pedido.grado_urgencia if detalle_pedido.grado_urgencia is not None else "N/A"
                cantidad_piezas = detalle_pedido.cantidad_piezas if detalle_pedido.cantidad_piezas is not None else "N/A"
                cantidad_trozos = detalle_pedido.cantidad_trozos if detalle_pedido.cantidad_trozos is not None else "N/A"
                piezas_xpaquete = detalle_pedido.piezas_xpaquete if detalle_pedido.piezas_xpaquete is not None else "N/A"
                piezas_xtrozo = detalle_pedido.piezas_xtrozo if detalle_pedido.piezas_xtrozo is not None else "N/A"
                paquetes_solicitados = detalle_pedido.paquetes_solicitados if detalle_pedido.paquetes_solicitados is not None else "N/A"
                volumen_obtenido = detalle_pedido.volumen_obtenido if detalle_pedido.volumen_obtenido is not None else "N/A"
                paquetes_saldo = detalle_pedido.paquetes_saldo if detalle_pedido.paquetes_saldo is not None else "N/A"
                diametro_rollizo = producto.nombre_rollizo.diametro if producto.nombre_rollizo else "N/A"
                try:
                    patron_corte_data = PatronCorte.objects.get(rollizo=producto.nombre_rollizo)
                    codigo_patron = patron_corte_data.codigo
                    nombre_patron = patron_corte_data.nombre
                    descripcion_patron = patron_corte_data.descripcion
                    rendimiento_patron = patron_corte_data.rendimiento
                    velocidad_linea_patron = patron_corte_data.velocidad_linea
                    setup_time_patron = patron_corte_data.setup_time
                    lead_time_patron = patron_corte_data.lead_time
                    utilizado_patron = str(patron_corte_data.utilizado)
                    producto_asociado_patron = patron_corte_data.producto_asociado
                except PatronCorte.DoesNotExist:
                    codigo_patron = "N/A"
                    nombre_patron = "N/A"
                    descripcion_patron = "N/A"
                    rendimiento_patron = "N/A"
                    velocidad_linea_patron = "N/A"
                    setup_time_patron = "N/A"
                    lead_time_patron = "N/A"
                    utilizado_patron = "N/A"
                    producto_asociado_patron = "N/A"


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
                    producto_codigo,  #9 
                    largo, #10
                    ancho, # 11
                    alto, # 12
                    nombre_linea, # 13
                    color,  # 14
                    color_p,  # 15
                    descripcion,# 16
                    inventario_inicial,# 17
                    valor_inventario,# 18   
                    costo_almacenamiento,# 19
                    nombre_rollizo,# 20
                    patron_corte,# 21
                    alto_producto,  # 22
                    ancho_producto,  # 23
                    largo_producto,  # 24
                    volumen_producto,  # 25
                    estado_pedido_linea,  # 26
                    grado_urgencia,  # 27
                    cantidad_piezas,  # 28
                    cantidad_trozos,  # 29
                    piezas_xpaquete,  #30
                    piezas_xtrozo,  # 31
                    paquetes_solicitados,  # 32
                    volumen_obtenido,  # 33
                    paquetes_saldo, # 34
                    diametro_rollizo, # 35
                    codigo_patron,  # 36
                    nombre_patron,  # 37
                    descripcion_patron,  # 38
                    rendimiento_patron,  # 39
                    velocidad_linea_patron,  # 40
                    setup_time_patron,  # 41
                    lead_time_patron,  # 42
                    utilizado_patron,  # 43
                    producto_asociado_patron,  # 44
                ]

                tasks.append(tasks_pedido)
        else:
            # Si no hay productos asociados al pedido, se crea una entrada con valores predeterminados
            productos_name = ["N/A"]
            producto_codigo = ["N/A"]
            color = random.choice(colores)
            color_p = prioridad_colores.get(pedido.prioridad, '#4287f5')
            porcentaje_progreso = random.randint(10, 100)
            nombre_cliente = pedido.cliente.nombre_cliente if pedido.cliente else "N/A"  # "N/A" si no hay cliente
            tasks_pedido = [
                pedido.orden_pedido,
                fecha_actual,   # 1
                pedido.fecha_entrega.strftime('%Y/%m/%d'),  # 2
                pedido.fecha_produccion.strftime('%Y/%m/%d'),  # 3
                porcentaje_progreso,  # 4
                nombre_cliente,  # 5
                productos_name,  # 6
                producto_codigo,  # 7
                color,  # 11
                color_p,  # 12
            
            ]

            tasks.append(tasks_pedido)
    context = {
    'tasks': tasks,
    'pedido_form': pedido_form,  # Include the pedido_form in the context
    'detalle_pedido_formset': detalle_pedido_formset,  # Include the detalle_pedido_formset in the context
    }
    return render(request, 'home.html', context)


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




def linea(request):
    lineas = Linea.objects.all()
    form = CrearLineaForm()

    if request.method == 'POST':
        if 'crear' in request.POST:
            form = CrearLineaForm(request.POST)
            if form.is_valid():
                nueva_linea = form.save()
                print("Producto guardado en la base de datos con ID:", nueva_linea.id)  # Mensaje de depuración
                return redirect('plan_linea')
    
    context = {
        'form': form,
        'lineas': lineas
    }
    return render(request, 'planificador/planificador_linea.html', context)


def rollizo(request):
    rollizos = Rollizo.objects.all()
    form = CrearRollizoForm()

    if request.method == 'POST':
        if 'crear' in request.POST:
            form = CrearRollizoForm(request.POST)
            if form.is_valid():
                nuevo_rollizo = form.save()
                print("Producto guardado en la base de datos con ID:", nuevo_rollizo.id)  # Mensaje de depuración
                return redirect('plan_rollizo')
    
    context = {
        'form': form,
        'rollizos': rollizos
    }
    return render(request, 'planificador/planificador_rollizo.html', context)


def eliminar_rollizo(request,id):
    rollizo=Rollizo.objects.get(id=id)
    rollizo.delete()
    return redirect('plan_rollizo')

def eliminar_linea(request,id):
    linea=Linea.objects.get(id=id)
    linea.delete()
    return redirect('plan_linea')
 

def cliente(request):
    clientes = Cliente.objects.all()
    form = CrearClienteForm()

    if request.method == 'POST':
        if 'crear' in request.POST:
            form = CrearClienteForm(request.POST)
            if form.is_valid():
                nueva_cliente = form.save()
                print("Producto guardado en la base de datos con ID:", nueva_cliente.id)  # Mensaje de depuración
                return redirect('admin_cliente')
    
    context = {
        'form': form,
        'clientes': clientes
    }
    return render(request, 'admin/admin_cliente.html', context)


def empresa(request):
    empresas = Empresa.objects.all()
    form = CrearEmpresaForm()

    if request.method == 'POST':
        if 'crear' in request.POST:
            form = CrearEmpresaForm(request.POST)
            if form.is_valid():
                nueva_empresa = form.save()
                return redirect('admin_empresa')
    
    context = {
        'form': form,
        'empresas': empresas
    }
    return render(request, 'admin/admin_empresa.html', context)


def eliminar_cliente(request,id):
    cliente=Cliente.objects.get(id=id)
    cliente.delete()
    return redirect('admin_cliente')


def eliminar_empresa(request,id):
    empresa=Empresa.objects.get(id=id)
    empresa.delete()
    return redirect('admin_empresa')