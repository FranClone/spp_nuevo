"""En este módulo se definen todas las vistas para la aplicación web y la lógica para las solicitudes HTTP. 
Maneja las request del usuario y responde con contenido como páginas HTML, JSON, entre otros.
En Django, una vista es una función de Python o basada en clases que toma una web request y devuelve una web response.
Las vistas están típicamente asociadas con una URL en el módulo 'urls.py'.
"""
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views.generic import View, CreateView
from django.http import JsonResponse, FileResponse, Http404
#from asignaciones.models import UserProfile
from .forms import CustomUserCreationForm,ActualizarStockRollizo, DetallePedidoForm,LoginForm, ActualizarMateriaPrimaForm,StockForm, CrearProductoForm ,CrearPatronCorteForm, ActualizarPedidoForm, CrearLineaForm, CrearRollizoForm, CrearClienteForm, CrearEmpresaForm
from .modelos.patron_corte import PatronCorte
from .modelos.producto import Producto
from .modelos.pedidos import Pedido
from .modelos.rollizo import Rollizo
from .modelos.linea import Linea
from .modelos.detalle_pedido import DetallePedido
from .modelos.cliente import Cliente
from .modelos.empresa import Empresa
from .modelos.materia_prima import MateriaPrima
from .modelos.stock_producto import StockProducto
from django.forms import inlineformset_factory
from .modelos.detalle_pedido import DetallePedido
from .modelos.factura import Factura
from .modelos.empaque import Empaque
from .modelos.stock_rollizo import StockRollizo
from .modelos.medida import Medida
from .models import Usuario

#from .pedidoForm import PedidoForm, DetallePedidoForm, DetallePedidoFormSet
from .queries import sel_cliente_admin, sel_pedido_empresa, sel_empresa_like, sel_pedido_productos_empresa, insertar_pedido, insertar_detalle_pedido, sel_rollizo_empresa, sel_bodega_empresa, sel_linea_empresa, sel_producto_empresa, cantidad_pedidos_por_mes
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
import pandas as pd
import logging  # Import the logging module
from django.db import IntegrityError
from mip import Model,maximize,CBC,BINARY,xsum
from django.http import JsonResponse
from .roles import require_role
from .forms import ActualizarPedidoForm, DetallePedidoForm
from django.db import transaction

#
try:
    #se conecta
    conexion = pyodbc.connect(os.environ.get('CONEXION_BD'))
    print("Conexión a base de datos exitosa")

except Exception as ex:
    print(ex)


#TEST ALGORITMO 
def solver_betech(archivo1, archivo2):
    try:
        archivo1 = os.path.join(settings.MEDIA_ROOT, "LineaDelgado.csv")
        archivo2 = os.path.join(settings.MEDIA_ROOT, "LineaGruesa.csv")

        df_linea_delgada = pd.read_csv(archivo1, encoding="latin-1", sep=";")
        df_linea_gruesa = pd.read_csv(archivo2, encoding="latin-1", sep=";")
        columns_names = df_linea_delgada.columns.values

        diametro = df_linea_delgada[df_linea_delgada.columns.values[18]]
        print("****************************************")
        print("LECTURA ARCHIVO LINEA GRUESA")
        print("****************************************")
        print(df_linea_gruesa.head())
        
        p = [10, 13, 18, 31, 7, 15]
        w = [11, 15, 20, 35, 10, 33]
        c, I = 47, range(len(w))
        
        m = Model('mochila', maximize, CBC)
        x = [m.add_var(var_type=BINARY) for i in I]
        m.objective = maximize(xsum(p[i] * x[i] for i in I))
        m += xsum(w[i] * x[i] for i in I) <= c
        m.optimize()
        selected = [i for i in I if x[i].x >= 0.99]
        print(diametro)
        return diametro,selected   
        # results = {
        #     'diametro': diametro.tolist(),  # Convert to a list if it's a Pandas Series
        #     'selected': selected
        # }
        
        # return JsonResponse(results)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Handle the error appropriately
 
        return None, None  # Return some default values o

def execute_code(request, archivo1, archivo2):
    # Call the solver_betech function to get results
    diametro, selected = solver_betech(archivo1, archivo2)

    # Convert the diametro Series to a list
    diametro_list = diametro.tolist()
    

    # Create a dictionary with the results
    results = {
        'diametro': diametro_list,
        'selected': selected
    }

    return JsonResponse(results)



def importar(request):
    alert_message = None  # Inicialmente, no hay mensaje de alerta
    success = False  # Inicialmente, no se considera éxito

    if request.method == 'POST':
        # Verifica si el archivo 'xlsfile' está presente en 'request.FILES'
        if 'xlsfile' in request.FILES:
            xlsfile = request.FILES['xlsfile']
            result = process_uploaded_file(request,xlsfile)
            if result.get('success'):
                # Importación exitosa, muestra un mensaje de éxito
                success = True
                alert_message = 'Importacion exitosa'
            else:
                # Importación fallida, muestra un mensaje de error
                alert_message = 'Error: ' + (result.get('error_message') or '')
        else:
            alert_message = "No se ha seleccionado ningún archivo para subir."

        return render(request, 'aviso.html', {'alert_message': alert_message, 'success': success})
        

def process_uploaded_file(request,xlsfile):
    success = False
    error_message = None
    if not xlsfile:
        error_message = "No se ha seleccionado ningún archivo para subir."
    else:
        try:
            # Cargar el archivo Excel en un DataFrame de pandas
            df = pd.read_excel(xlsfile)
            # #Obtener la empresa, a la que pertenece el usuario que carga el pedido para agregarlo al producto nuevo    
            # nombre_empresa = request.user.empresa
            # print(nombre_empresa)
            # empresa = Empresa.objects.get(nombre_empresa=nombre_empresa)
            # rut_empresa_usuario = empresa.rut_empresa 
            # print(rut_empresa_usuario)
            # #Obtener el id de rollizo de los productos ya agregados
            # productos_existentes = Producto.objects.all().values('nombre', 'nombre_rollizo_id', 'linea_id')
            # id_rollizos_existentes = {producto['nombre']: producto['nombre_rollizo_id'] for producto in productos_existentes}
            # #Obtener el id de linea de los productos ya agregados
            # id_lineas_existentes = {producto['nombre']: producto['linea_id'] for producto in productos_existentes}
            with transaction.atomic():
                # Use a transaction to ensure data integrity

                # Crear una instancia de Pedido para cada registro y guardarla en la base de datos
                for index, row in df.iterrows():
                    productos_str = str(row['producto'])  # Convert 'producto' to a string
                    if productos_str and isinstance(productos_str, str):
                        productos_list = [producto.strip() for producto in productos_str.split(',')]  # Split and clean product names
                        
                        id_cliente = row['cliente']
                        cliente = Cliente.objects.get(id=id_cliente)
                        pedido = Pedido(
                            cliente=cliente,
                            fecha_produccion=row['fecha_produccion'],
                            fecha_entrega=row['fecha_entrega'],
                            orden_interna=row['op'],
                            comentario=row['comentario'],
                            #prioridad=row['prioridad'],#agregar para editar en la pagina null=false
                            version=row['version'],
                            estado=row['estado']#agregar para editar en la pagina null=false
                        )
                        pedido.save()
                        factura = Factura(
                            FSC=row['FSC'],  
                            esp_fact=row['esp_fact'], 
                            anc_fact=row['anc_fact'],  
                            lar_fact=row['lar_fact']  
                        )
                        factura.save()
                        empaque = Empaque(
                            pqte=row['pqte'],  
                            tipo_empaque=row['tipo_empaque'],  
                            alto_paquete=row['alto_paquete'],  
                            anc_paquete=row['anc_paquete'],  
                            int_paquete=row['int_paquete']  
                        )
                        empaque.save()
                        for producto_nombre in productos_list:
                            try:
                                producto = Producto.objects.get(nombre=producto_nombre)

                                # Verificar si se han proporcionado medidas diferentes a las que ya existen
                                alto = row['alto']
                                ancho = row['ancho']
                                largo = row['largo']
                                # Buscar o crear la medida
                                medida, _ = Medida.objects.get_or_create(
                                    alto_producto=alto,
                                    ancho_producto=ancho,
                                    largo_producto=largo,
                                )
                                # Asociar la medida con el producto
                                if medida not in producto.medida.all():
                                    producto.medida.add(medida)
                            except Producto.DoesNotExist:
                                print(f"El producto {producto_nombre} no existe en la base de datos.")
                            # if producto_nombre in id_rollizos_existentes and id_lineas_existentes:
                            #     id_rollizo = id_rollizos_existentes[producto_nombre]
                            #     id_linea = id_lineas_existentes[producto_nombre]
                            #     print("id rollizo encontrado>", id_rollizo,id_linea)
                            # else:
                            #     id_rollizo = 1 
                            #     id_linea=1# Aquí debes definir el valor adecuado

                            # Busca el producto por nombre
                            # producto, created = Producto.objects.get_or_create(nombre=producto_nombre, empresa_id=rut_empresa_usuario, nombre_rollizo_id=id_rollizo, linea_id=id_linea, inventario_inicial=0, inventario_final=0)

                            # Verifica si se han proporcionado medidas diferentes a las que ya existen
                            # alto = row['alto']
                            # ancho = row['ancho']
                            # largo = row['largo']
                            # medida, _ = Medida.objects.get_or_create(
                            #     alto_producto=alto,
                            #     ancho_producto=ancho,
                            #     largo_producto=largo,
                            # )
                            # if created:
                            #     # Asocia la medida con el nuevo producto si se ha creado
                            #     producto.medida.add(medida)
                            #     print(producto, "creado")
                            # else:
                            #     # Comprueba si la medida existe en el producto y si no, la asocia
                            #     if medida not in producto.medida.all():
                            #         producto.medida.add(medida)
                            #         print(producto, medida, "asociado")
                            detalle_pedido = DetallePedido(
                                pedido=pedido,
                                producto=producto,
                                factura=factura,
                                empaque=empaque,
                                item=row['item'],
                                #folio=row['folio'], # agregar para editar en la pagina null=True
                                alto_producto=row['alto'],
                                ancho_producto=row['ancho'],
                                largo_producto=row['largo'],
                                volumen_producto=row['M3'],
                                fecha_entrega=row['fecha_entrega'],
                                #grado_urgencia=row['prioridad'], #agregar para editar en la pagina null=True
                                cantidad_piezas=row['piezas'], 
                                #cantidad_trozos=row['cantidad_trozos'], #??? 
                                #piezas_xpaquete=row['piezas_xpaquete'], #???
                                #piezas_xtrozo=row['piezas_xtrozo'], #???
                                #paquetes_solicitados=row['paquetes_solicitados'], #???
                                #paquetes_saldo=row['paquetes_saldo'], #???
                                detalle_producto=row['comentario'],
                                mercado=row['mercado'],
                                puerto_destino=row['puerto_destino'],
                                term=row['term'],
                                calidad=row['calidad'],
                                mbf=row['mbf'],
                                banio=row['baño'],
                                marca=row['marca'],
                                programa=row['programa'],
                                piezas=row['piezas'],
                                cpo=row['cpo'],
                                piezas_x_cpo=row['piezas_x_cpo'],
                                est=row['Est']
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
                        success = True
                print("Importación exitosa.")
        except IntegrityError as e:
            error_message = "Error de integridad de datos: Verifica duplicados o datos faltantes."
            print(f"IntegrityError: {e}")
        except ValueError as e:
            error_message = "Error de formato de datos: Verifica los tipos de datos esperados."
            print(f"ValueError: {e}")
        except Cliente.DoesNotExist:
            error_message = (f"Cliente con id {id_cliente} no existe.")
        except Producto.DoesNotExist:
            print(f"Uno o más productos especificados no existen: {productos_str}")
            error_message = "Uno o más productos especificados no existen:"
        except Exception as e:
            error_message = "Error desconocido en la importación de datos: " + str(e)
            print(f"Excepción desconocida: {e}")
        else:
            error_message = "Error desconocido en la importación de datos"

        # Código adicional aquí

        return {'success': success, 'error_message': error_message}


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
    @method_decorator(login_required)
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

# class Inventario_roll(View):
#     @method_decorator(login_required) 
#     def get(self, request, *args, **kwargs):
#         #lista de clases diamétricas, desde 14 hasta 40
#         clase_diametrica = list(range(14, 41, 2))
#         rut_empresa = request.user.empresa.rut_empresa
#         clas = sel_rollizo_clasificado_empresa(rut_empresa)
#         noclas = sel_rollizo_empresa(rut_empresa)
#         return render(request, 'inventario_rollizo.html', {"clase_diametrica": clase_diametrica, "clas":clas, "noclas":noclas})

class Pedidos(View):
    @require_role(['ADMINISTRADOR', 'PLANIFICADOR'])  
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'pedidos.html') 


class Lista_pedidos(View): 
    @require_role(['ADMINISTRADOR', 'PLANIFICADOR'])   
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'lista_pedidos.html', context)
    
class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    
    
    #verifica si la solicitud HTTP es de tipo POST
    def post(self, request):
        
        if request.method == 'POST':
            print(request.POST)
            #Se obtienen los valores del campo "Rut" y "contraseña" del formulario
            username = request.POST.get('username')
            password = request.POST.get('password')
            #autenticar al usuario utilizando el valor del campo "Rut" como nombre de usuario y el valor del campo "contraseña"
            user = authenticate(request, username=username, password=password)
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
        return render(request, 'login.html')
    

class Logout(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class Mantenedor(View): 
    
    """Esta clase define la vista de Mantenedor"""
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'mantenedor.html', context)

class Register(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})



class Plan_Patrones_Corte(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'planificador/planificador_patrones_corte.html')

class Plan_Productos(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'planificador/planificador_productos.html')



#@method_decorator(login_required, name='dispatch')
@method_decorator(require_role(['ADMINISTRADOR', 'PLANIFICADOR']), name='dispatch')        
class Dashboard(View): 
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html')

@require_role('ADMINISTRADOR')    
@login_required
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

@require_role('ADMINISTRADOR')  
@login_required
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
                
                # Obtén los patrones de corte seleccionados en el formulario
                patrones_de_corte = request.POST.getlist('patron_corte')
                
                # Agrega los patrones de corte al producto
                for patron_id in patrones_de_corte:
                    patron_corte = PatronCorte.objects.get(pk=patron_id)
                    nuevo_producto.patron_corte.add(patron_corte)
                
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


@require_role('ADMINISTRADOR')  
@login_required
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

@require_role('ADMINISTRADOR')  
@login_required
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

@login_required
def pantalla_carga(request):
    rol = request.user.roles
    return render(request, 'pantalla-carga.html',{'rol': rol})


@require_role(['ADMINISTRADOR', 'PLANIFICADOR'])
@login_required
def pedidos(request):
    pedidos = Pedido.objects.all()
    DetallePedidoFormSet = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        pedido_form = ActualizarPedidoForm(request.POST)
        detalle_pedido_formset = DetallePedidoFormSet(request.POST, prefix='detalle_pedido')
        print("post pedido")
        print("Before pedido_form validation")
        if pedido_form.is_valid():
            print("pedido_form is valid")
        else:
            print("pedido_form is NOT valid")
            print(pedido_form.errors)
        if detalle_pedido_formset.is_valid():
            print("detalle_pedido_formset is valid")
        else:
            print("detalle_pedido_formset is NOT valid")
            print(detalle_pedido_formset.errors)
            
        if pedido_form.is_valid() and detalle_pedido_formset.is_valid():
            print("formulario valido")
            with transaction.atomic():
                pedido_instance = pedido_form.save()
                producto_seleccionado = pedido_form.cleaned_data['producto']
                # producto_elegido = pedido_form.cleaned_data.get('producto')
                # pedido_instance.producto = producto_elegido
                # pedido_instance.save()
                primera_form = detalle_pedido_formset.forms[0]
                print(primera_form)
                factura_data = {
                    'FSC': primera_form.cleaned_data.get('FSC'),
                    'esp_fact': primera_form.cleaned_data.get('esp_fact'),
                    'anc_fact': primera_form.cleaned_data.get('anc_fact'),
                    'lar_fact': primera_form.cleaned_data.get('lar_fact'),
                }
                factura_instance = Factura(**factura_data)
                factura_instance.save()
                print(factura_instance)
                empaque_data = {
                    'pqte': primera_form.cleaned_data.get('pqte'),
                    'tipo_empaque': primera_form.cleaned_data.get('tipo_empaque'),
                    'alto_paquete': primera_form.cleaned_data.get('alto_paquete'),
                    'int_paquete': primera_form.cleaned_data.get('int_paquete'),
                    'anc_paquete': primera_form.cleaned_data.get('anc_paquete'),
                }   
                empaque_instance = Empaque(**empaque_data)
                empaque_instance.save()           
                # Create and save a new Factura instance with the extracted data

                print(empaque_instance)
                print(f"Factura: {factura_instance}")
                print(f"Empaque: {empaque_instance}")
                print(f"Pedido: {pedido_instance}")
                # Loop through DetallePedido forms in the formset
                for detalle_pedido_form in detalle_pedido_formset:
                    detalle_pedido_instance = detalle_pedido_form.save(commit=False)
                    detalle_pedido_instance.pedido = pedido_instance
                    detalle_pedido_instance.factura = factura_instance
                    detalle_pedido_instance.empaque = empaque_instance
                    detalle_pedido_instance.producto = producto_seleccionado
                    detalle_pedido_instance.fecha_entrega = pedido_instance.fecha_entrega  # Set fecha_entrega based on the associated Pedido
                    detalle_pedido_instance.save()



            return redirect('home')
        else:
            # Imprime los errores del formulario en la consola
            for form in detalle_pedido_formset:
                if form.errors:
                    print(f"Errores en el formulario: {form.errors}")
                    print(detalle_pedido_formset.errors)

    else:
        pedido_form = ActualizarPedidoForm()
        detalle_pedido_formset = DetallePedidoFormSet(prefix='detalle_pedido')

    context = {
        'pedido_form': pedido_form,
        'detalle_pedido_formset': detalle_pedido_formset,
        'pedidos': pedidos,  # Agrega los pedidos al contexto
    
    }

    return render(request, 'pedidos.html', context)

@require_role(['ADMINISTRADOR', 'PLANIFICADOR'])
@login_required
def gantt_view(request):
    
    pedido_form = ActualizarPedidoForm()
    DetallePedidoFormSet = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=1, can_delete=True)
    detalle_pedido_formset = DetallePedidoFormSet(prefix='detalle_pedido')

    pedidos = Pedido.objects.all()

    fecha_actual = datetime.today().strftime('%Y/%m/%d')
    #
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
        pedido_id = pedido.id
        if productos.exists():
            for producto in productos:
                productos_name = [producto.nombre]
                producto_codigo = [producto.orden_producto]
                porcentaje_progreso = random.randint(10, 100)
                nombre_cliente = pedido.cliente.nombre_cliente if pedido.cliente else "N/A"  # "N/A" si no hay cliente
                nombre_linea = producto.linea.nombre_linea
                color = random.choice(colores)
                color_p = prioridad_colores.get(pedido.prioridad, '#4287f5')
                descripcion = producto.descripcion
                inventario_inicial = producto.inventario_inicial
                nombre_rollizo = producto.nombre_rollizo.nombre_rollizo if producto.nombre_rollizo else "N/A"
                patron_corte = [pc.nombre for pc in producto.patron_corte.all()] if producto.patron_corte.exists() else ["N/A"]
                detalle_pedido = DetallePedido.objects.get(pedido=pedido, producto=producto)
                mercado = detalle_pedido.mercado if detalle_pedido.mercado is not None else "N/A"
                destino = detalle_pedido.puerto_destino if detalle_pedido.mercado is not None else "N/A"
                item = detalle_pedido.item if detalle_pedido.item is not None else "N/A"
                folio = detalle_pedido.folio if detalle_pedido.folio is not None else "N/A"
                alto_producto = detalle_pedido.alto_producto if detalle_pedido.alto_producto is not None else "N/A"
                ancho_producto = detalle_pedido.ancho_producto if detalle_pedido.ancho_producto is not None else "N/A"
                largo_producto = detalle_pedido.largo_producto if detalle_pedido.largo_producto is not None else "N/A"
                volumen_producto = detalle_pedido.volumen_producto if detalle_pedido.volumen_producto is not None else "N/A"
                estado = pedido.estado if pedido.estado is not None else "N/A"
                #estado_pedido_linea = detalle_pedido.estado_pedido_linea if detalle_pedido.estado_pedido_linea is not None else "N/A"
                grado_urgencia = detalle_pedido.grado_urgencia if detalle_pedido.grado_urgencia is not None else "N/A"
                cantidad_piezas = detalle_pedido.cantidad_piezas if detalle_pedido.cantidad_piezas is not None else "N/A"
                cantidad_trozos = detalle_pedido.cantidad_trozos if detalle_pedido.cantidad_trozos is not None else "N/A"
                piezas_xpaquete = detalle_pedido.piezas_xpaquete if detalle_pedido.piezas_xpaquete is not None else "N/A"
                piezas_xtrozo = detalle_pedido.piezas_xtrozo if detalle_pedido.piezas_xtrozo is not None else "N/A"
                paquetes_solicitados = detalle_pedido.paquetes_solicitados if detalle_pedido.paquetes_solicitados is not None else "N/A"
                volumen_obtenido = detalle_pedido.volumen_obtenido if detalle_pedido.volumen_obtenido is not None else "N/A"
                paquetes_saldo = detalle_pedido.paquetes_saldo if detalle_pedido.paquetes_saldo is not None else "N/A"
                diametro_rollizo = producto.nombre_rollizo.diametro if producto.nombre_rollizo else "N/A"
                term = detalle_pedido.term if detalle_pedido.term is not None else "N/A"
                calidad = detalle_pedido.calidad if detalle_pedido.calidad is not None else "N/A"
                mbf = detalle_pedido.mbf if detalle_pedido.mbf is not None else "N/A"
                banio = detalle_pedido.banio if detalle_pedido.banio is not None else "N/A"
                marca = detalle_pedido.marca if detalle_pedido.marca is not None else "N/A"
                programa = detalle_pedido.programa if detalle_pedido.programa is not None else "N/A"
                piezas = detalle_pedido.piezas if detalle_pedido.piezas is not None else "N/A"
                cpo = detalle_pedido.cpo if detalle_pedido.cpo is not None else "N/A"
                piezas_x_cpo = detalle_pedido.piezas_x_cpo if detalle_pedido.piezas_x_cpo is not None else "N/A"
                est = detalle_pedido.est if detalle_pedido.est is not None else "N/A"
                largo_rollizo = producto.nombre_rollizo.largo or "N/A"
                factura = Factura.objects.get(pk=detalle_pedido.factura.pk)
                FSC = factura.FSC if factura.FSC is not None else "N/A"
                esp_fact = factura.esp_fact if factura.esp_fact is not None else "N/A"
                anc_fact = factura.anc_fact if factura.anc_fact is not None else "N/A"
                lar_fact = factura.lar_fact if factura.lar_fact is not None else "N/A"
                # Añade los atributos de Empaque
                empaque = Empaque.objects.get(pk=detalle_pedido.empaque.pk)
                pqte = empaque.pqte if empaque.pqte is not None else "N/A"
                tipo_empaque = empaque.tipo_empaque if empaque.tipo_empaque is not None else "N/A"
                alto_paquete = empaque.alto_paquete if empaque.alto_paquete is not None else "N/A"
                int_paquete = empaque.int_paquete if empaque.int_paquete is not None else "N/A"
                anc_paquete = empaque.anc_paquete if empaque.anc_paquete is not None else "N/A"
                try:
                    patron_corte_data = PatronCorte.objects.get(rollizo=producto.nombre_rollizo)
                    codigo_patron = patron_corte_data.codigo
                    nombre_patron = patron_corte_data.nombre
                    descripcion_patron = patron_corte_data.descripcion
                    rendimiento_patron = patron_corte_data.rendimiento

                    utilizado_patron = str(patron_corte_data.utilizado)

                  #  producto_asociado_patron = patron_corte_data.producto_asociado

                except PatronCorte.DoesNotExist:
                    codigo_patron = "N/A"
                    nombre_patron = "N/A"
                    descripcion_patron = "N/A"
                    rendimiento_patron = "N/A"
                    utilizado_patron = "N/A"

                  #  producto_asociado_patron = "N/A"

                tasks_pedido = [
                    pedido.orden_interna,
                    fecha_actual,   # 1
                    pedido.fecha_entrega.strftime('%Y/%m/%d'),  # 2
                    pedido.fecha_produccion.strftime('%Y/%m/%d'),  # 3
                    porcentaje_progreso,  # 4
                    nombre_cliente,  # 5
                    pedido.comentario,  # 6
                    productos_name,  # 7
                    pedido.prioridad,  # 8
                    producto_codigo,  #9 
                    nombre_linea, #10
                    color, #11
                    color_p, #12
                    descripcion, #13
                    inventario_inicial, #14
                    nombre_rollizo, #15
                    patron_corte, #16
                    alto_producto, #17
                    ancho_producto, #18
                    largo_producto, #19
                    volumen_producto, #20
                    estado, #21
                    grado_urgencia, #22
                    cantidad_piezas, #23
                    cantidad_trozos, #24
                    piezas_xpaquete, #25
                    piezas_xtrozo, #26
                    paquetes_solicitados, #27
                    volumen_obtenido, #28
                    paquetes_saldo, #29
                    diametro_rollizo, #30
                    codigo_patron, #31
                    nombre_patron, #32
                    descripcion_patron, #33
                    rendimiento_patron, #34
                    utilizado_patron, #35
                    item, #36
                    folio, #37
                    mercado, #38
                    destino, #39
                    largo_rollizo, #40
                    FSC, #41
                    esp_fact, #42
                    anc_fact, #43
                    lar_fact, #44
                    pqte, #45
                    tipo_empaque, #46
                    alto_paquete, #47
                    int_paquete, #48
                    term, #49
                    calidad, #50
                    mbf, #51
                    banio, #52
                    marca, #53
                    programa, #54
                    piezas, #55
                    cpo, #56
                    piezas_x_cpo, #57
                    anc_paquete, #58
                    est, #59
                    pedido_id, #60
                ]

                tasks.append(tasks_pedido)
    formStockRollizo = ActualizarStockRollizo()
    formstockterminado = StockForm()
    context = {
    'tasks': tasks,
    'pedido_form': pedido_form,  # Include the pedido_form in the context
    'detalle_pedido_formset': detalle_pedido_formset, 
    'formStockRollizo':formStockRollizo,
    'formstockterminado':formstockterminado # Include the detalle_pedido_formset in the context
    }
    print("hola")
    return render(request, 'home.html', context)

@require_role('ADMINISTRADOR')  
@login_required
def eliminar_materia_prima(request,id):
    materia_prima=MateriaPrima.objects.get(id=id)
    materia_prima.eliminar()

    return redirect('plan_materia_prima')

@require_role('ADMINISTRADOR')  
@login_required
def eliminar_pedido(request,id):
    pedido=Pedido.objects.get(id=id)
    pedido.eliminar()

    return redirect('pedidos')

@require_role('ADMINISTRADOR')  
@login_required
def eliminar_patron(request,id):
    patron=PatronCorte.objects.get(id=id)
    patron.eliminar()

    return redirect('plan_patrones_corte')

@require_role('ADMINISTRADOR')  
@login_required
def eliminar_producto(request,id):
    producto=Producto.objects.get(id=id)
    producto.eliminar()
    return redirect('plan_productos')

@require_role('ADMINISTRADOR')  
@login_required
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
    

@require_role('ADMINISTRADOR')  
@login_required
def linea_editar(request,id):
    prod= Linea.objects.get(id=id)
    data = {'form': CrearLineaForm(instance=prod),'id':id}
    if request.method == 'POST':
        formulario = CrearLineaForm(data = request.POST, instance=prod)
        if formulario.is_valid():
            formulario.save()
            return redirect('plan_linea')
        else:
            print("error")
    return render(request, 'planificador/planificador_lineaeditar.html', data)

@require_role('ADMINISTRADOR')  
@login_required
def rollizo_editar(request,id):
    prod= Rollizo.objects.get(id=id)
    data = {'form': CrearRollizoForm(instance=prod),'id':id}
    if request.method == 'POST':
        formulario = CrearRollizoForm(data = request.POST, instance=prod)
        if formulario.is_valid():
            formulario.save()
            return redirect('plan_rollizo')
        else:
            print("error")
    return render(request, 'planificador/planificador_rollizoeditar.html', data)

@require_role('ADMINISTRADOR')  
@login_required
def pedido_editar(request, id):
    prod = Pedido.objects.get(id=id)
    DetallePedidoFormSet = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=0, can_delete=True)

    detalle_pedido = DetallePedido.objects.filter(pedido=prod).first()
    factura = None
    paquete = None

    if detalle_pedido:
        factura = detalle_pedido.factura
        paquete = detalle_pedido.empaque
        detalle_pedido_id = detalle_pedido.id

    data = {}

    if request.method == 'POST':
        pedido_form = ActualizarPedidoForm(request.POST, instance=prod)
        detalle_pedido_formset = DetallePedidoFormSet(request.POST, instance=prod, prefix=f'detalle_pedido_{detalle_pedido_id}')

        if pedido_form.is_valid() and detalle_pedido_formset.is_valid():
            pedido_form.save()

            # Obtener la instancia de Factura y Empaque existentes o crear una nueva si no existen
            if factura:
                factura_form = detalle_pedido_formset.forms[0]  # El primer formulario en el formset
                factura_data = {
                    'FSC': factura_form.cleaned_data.get('FSC'),
                    'esp_fact': factura_form.cleaned_data.get('esp_fact'),
                    'anc_fact': factura_form.cleaned_data.get('anc_fact'),
                    'lar_fact': factura_form.cleaned_data.get('lar_fact'),
                }
                for field, value in factura_data.items():
                    setattr(factura, field, value)
                factura.save()
            if paquete:
                paquete_form = detalle_pedido_formset.forms[0]  # El primer formulario en el formset
                empaque_data = {
                    'pqte': paquete_form.cleaned_data.get('pqte'),
                    'tipo_empaque': paquete_form.cleaned_data.get('tipo_empaque'),
                    'alto_paquete': paquete_form.cleaned_data.get('alto_paquete'),
                    'int_paquete': paquete_form.cleaned_data.get('int_paquete'),
                    'anc_paquete': paquete_form.cleaned_data.get('anc_paquete'),
                }
                for field, value in empaque_data.items():
                    setattr(paquete, field, value)
                paquete.save()

            for detalle_pedido_form in detalle_pedido_formset:
                detalle_pedido_instance = detalle_pedido_form.save(commit=False)
                detalle_pedido_instance.factura = factura
                detalle_pedido_instance.empaque = paquete
                detalle_pedido_instance.save()

            return redirect('pedidos')
        else:
            print("Error in forms:", detalle_pedido_formset.errors)

    else:
        pedido_form = ActualizarPedidoForm(instance=prod)
        detalle_pedido_formset = DetallePedidoFormSet(instance=prod, prefix=f'detalle_pedido_{detalle_pedido_id}')

        for form in detalle_pedido_formset:
            if factura:
                form.fields['FSC'].initial = factura.FSC
                form.fields['esp_fact'].initial = factura.esp_fact
                form.fields['anc_fact'].initial = factura.anc_fact
                form.fields['lar_fact'].initial = factura.lar_fact
            if paquete:
                form.fields['pqte'].initial = paquete.pqte
                form.fields['tipo_empaque'].initial = paquete.tipo_empaque
                form.fields['alto_paquete'].initial = paquete.alto_paquete
                form.fields['int_paquete'].initial = paquete.int_paquete
                form.fields['anc_paquete'].initial = paquete.anc_paquete

    data['pedido_form'] = pedido_form
    data['detalle_pedido_formset'] = detalle_pedido_formset
    data['factura'] = factura
    data['paquete'] = paquete
    data['id'] = id
    data['detalle_pedido_id'] = detalle_pedido_id

    return render(request, 'pedidoseditar.html', data)


@require_role('ADMINISTRADOR')  
@login_required
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

@login_required
def obtener_ids_pedidos(request):
    ids_pedidos = Pedido.objects.values_list('id', flat=True)
    return JsonResponse({'ids_pedidos': list(ids_pedidos)})

@require_role(['ADMINISTRADOR', 'PLANIFICADOR'])
@login_required
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


@require_role('ADMINISTRADOR')  
@login_required
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
@require_role('ADMINISTRADOR')  
@login_required
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

@require_role('ADMINISTRADOR')  
@login_required
def eliminar_rollizo(request,id):
    rollizo=Rollizo.objects.get(id=id)
    rollizo.eliminar()
    return redirect('plan_rollizo')

@require_role('ADMINISTRADOR')  
@login_required
def eliminar_linea(request,id):
    linea=Linea.objects.get(id=id)
    linea.eliminar()
    return redirect('plan_linea')

@require_role('ADMINISTRADOR')  
@login_required
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

@require_role('BETECH')  
@login_required
def empresa(request):
    empresas = Empresa.objects.all()
    form = CrearEmpresaForm()

    if request.method == 'POST':
        if 'crear' in request.POST:
            form = CrearEmpresaForm(request.POST)
            if form.is_valid():
                nueva_empresa = form.save()
                print("Producto guardado en la base de datos con ID:", nueva_empresa.id)
                return redirect('admin_empresa')
    
    context = {
        'form': form,
        'empresas': empresas
    }
    return render(request, 'admin/admin_empresa.html', context)


@require_role('ADMINISTRADOR')  
@login_required
def eliminar_cliente(request,id):
    cliente=Cliente.objects.get(id=id)
    cliente.eliminar()
    return redirect('admin_cliente')

@require_role('BETECH') 
@login_required
def eliminar_empresa(request,id):
    empresa=Empresa.objects.get(rut_empresa=id)
    empresa.eliminar()
    return redirect('admin_empresa')


'''
def asignar_folio_pedido(request):
    if request.method == 'POST':
        # Obtiene el valor del folio del formulario POST
        texto_folio = request.POST.get('texto_folio')

        # Obtiene el ID del pedido del formulario POST
        pedido_id = request.POST.get('pedido_id')

        # Verifica si el texto_folio no está vacío
        if texto_folio:
            # Actualiza todos los detalles de pedidos asociados con el pedido ID
            DetallePedido.objects.filter(pedido_id=pedido_id).update(folio=texto_folio)
            alert_message = 'Se ha creado el folio'
            # Redirige a la página de éxito 'aviso.html'
            return render(request, 'aviso.html', {'alert_message': alert_message})  # Renderiza la página HTML de éxito
        else:
            # En caso de que el campo de texto esté vacío, muestra un mensaje de error
            alert_message = 'El campo de texto no puede estar vacío'

            return render(request, 'aviso.html', {'alert_message': alert_message})
    # Renderiza el formulario en una plantilla HTML

    return render(request, 'aviso.html')  # Renderiza la página HTML de formulario
'''
@require_role('ADMINISTRADOR')  
@login_required
def cliente_editar(request,id):
    cliente= Cliente.objects.get(id=id)
    data = {'form': CrearClienteForm(instance=cliente),'id':id}
    if request.method == 'POST':
        formulario = CrearClienteForm(data = request.POST, instance=cliente)
        if formulario.is_valid():
            formulario.save()
            return redirect('admin_cliente')
        else:
            print("error")
    return render(request, 'admin/admin_clienteeditar.html', data)


@require_role('BETECH')  
@login_required
def empresa_editar(request,id):
    empresa= Empresa.objects.get(rut_empresa=id)
    data = {'form': CrearEmpresaForm(instance=empresa),'rut_empresa':id}
    if request.method == 'POST':
        formulario = CrearEmpresaForm(data = request.POST, instance=empresa)
        if formulario.is_valid():
            formulario.save()
            return redirect('admin_empresa')
        else:
            print("error")
    return render(request, 'admin/admin_empresaeditar.html', data)

class Custom404View(View):
    def get(self, request, *args, **kwargs):
        return render(request, '404.html', status=404)
    
@require_role('ADMINISTRADOR')  
@login_required
def actualizar_stock_rollizo(request):
    stocks = StockRollizo.objects.all()
    formStockRollizo = ActualizarStockRollizo()
    if request.method == 'POST':
        if 'crear' in request.POST:
            formStockRollizo = ActualizarStockRollizo(request.POST)
            if formStockRollizo.is_valid():
                nuevo_stock = formStockRollizo.save()
                print("Producto guardado en la base de datos con ID:", nuevo_stock.id)
                return redirect('home')
    else:
        formStockRollizo = ActualizarStockRollizo()
    context = {
        'formStockRollizo': formStockRollizo,
        'stocks': stocks
    }
    print("chao")
    return render(request, 'home.html', context)

@require_role('ADMINISTRADOR')  
@login_required
def stock(request):
    stocks = StockProducto.objects.all()
    formstockterminado = StockForm()

    if request.method == 'POST':
        if 'crear' in request.POST:
            formstockterminado = StockForm(request.POST)
  
            if formstockterminado.is_valid():
                nuevo_stock = formstockterminado.save()
                print("Producto guardado en la base de datos con ID:", nuevo_stock.id)
                return redirect('plan_stock')
    
    context = {
        'form': formstockterminado,
        'stocks': stocks
    }
    return render(request, 'planificador/planificador_stock.html', context)

@require_role('ADMINISTRADOR')  
@login_required
def stock_editar(request,id):
    prod= StockProducto.objects.get(id=id)
    data = {'form': StockForm(instance=prod),'id':id}
    if request.method == 'POST':
        formulario = StockForm(data = request.POST, instance=prod)
        if formulario.is_valid():
            formulario.save()
            return redirect('plan_stock')
        else:
            print("error")
    return render(request, 'planificador/planificador_stockeditar.html', data)