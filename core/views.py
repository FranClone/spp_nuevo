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
from .forms import CustomUserCreationForm, LoginForm, ActualizarMateriaPrimaForm, CrearProductoForm, ProductoTerminadoForm, CrearPatronCorteForm
from .modelos.patron_corte import PatronCorte
from .modelos.producto import Producto
from .modelos.pedido import Pedido
from .modelos.empresa import Empresa
from .modelos.materia_prima import MateriaPrima
from .modelos.productos_terminados import ProductoTerminado
from .pedidoForm import PedidoForm, DetallePedidoForm, DetallePedidoFormSet
from .queries import sel_cliente_admin, sel_pedido_empresa, sel_empresa_like, sel_pedido_productos_empresa, insertar_pedido, insertar_detalle_pedido, sel_rollizo_clasificado_empresa, sel_rollizo_empresa, sel_bodega_empresa, sel_linea_empresa, sel_producto_empresa, cantidad_pedidos_por_mes
import pyodbc, json, os, datetime, openpyxl, bleach
from django.http import JsonResponse

# se intenta conectar a la base de datos
try:
    #se conecta
    conexion = pyodbc.connect(os.environ.get('CONEXION_BD'))
    print("conexión a base de datos exitosa")

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

class Home(View): 
    """Esta clase define la vista Home"""
    def get(self, request, *args, **kwargs):
        #cálculo progress
        producto_terminado = 1000
        producto_pedido = 5000
        progress = (producto_terminado / producto_pedido)*100
        
        return render(request, 'home.html')
    
    def post(self, request, *args, **kwargs):
        #Carga Archivo
        try:
            archivo = request.FILES['carga-masiva']
        except:
            return redirect('home')

        # Verifica el tamaño del archivo
        if archivo.size > 100000000:  # 100 MB
            #falta mensaje de error
            return redirect('home')

        # Carga el archivo utilizando openpyxl
        libro = openpyxl.load_workbook(archivo)
        hoja = libro.active
        # Itera sobre las filas de la hoja (a partir de la fila donde se encuentra "N°ORDEN")
        inicio_lectura = False
        datos_limpio = []

        for fila in hoja.iter_rows():
            # Ignora todas las filas hasta que se encuentra "N° ORDEN"
            if not inicio_lectura:
                if fila[0].value == "N° ORDEN":
                    inicio_lectura = True
                continue
            
            # Finaliza la lectura si la primera columna está vacía
            if not fila[0].value:
                break

            # Procesa los datos relevantes y aplica la limpieza con bleach
            fila_limpia = [bleach.clean(str(celda.value)) for celda in fila]
            datos_limpio.append(fila_limpia)

        # DE MOMENTO ESTE CÓDIGO TE DA LOS DATOS DE LA FILA LIMPIOS
        # FALTA AGREGAR LOS DATOS A LA BASE DE DATOS
        # VER COMO AGREGAR PRODUCTOS Y CLIENTE
        # ANALIZAR SI ES NECESARIO QUE PRODUCTOS Y CLIENTE ESTÉN PREVIAMENTE AGREGADOS
        # O SI SE AGREGA DIRECTAMENTE, CREAR EN DJANGO ORM CONSULTAS

        return redirect('home')

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
    form_class = LoginForm
    success_url = '/home/'
    def get(self, request):
        #Obtiene formulario de forms.py
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

    def post(self, request):
        #Obtiene rut desde el login
        rut_body = request.POST['rut_body']
        rut_dv = request.POST['rut_dv']
        rut = f'{rut_body}-{rut_dv}'
        password = request.POST['password']
        #Obtenemos el nombre de usuario desde el RUT
        def get_object_or_none(model, **kwargs):
            try:
                return model.objects.get(**kwargs)
            except model.DoesNotExist:
                return None
        #Buscamos nombre de usuario con el RUT ¿Por qué? Por que necesitamos
        #llamar a authenticate usando nombre de usuario y contraseña
        #Se aprovecha de la característica de que RUT, al igual que
        #Nombre de usuario, es único
        user_profile = get_object_or_none(UserProfile, rut=rut)
        #SIEMPRE llamar a authenticate, aunque no haya username que corresponda
        #Con el RUT, ya que AXES se activa al llamar a authenticate
        if user_profile is not None:
            username = user_profile.username
            user = authenticate(request, username=username, password=password)
        else:
            form = self.form_class(initial={'rut_body': rut_body, 'rut_dv': rut_dv})
            user = authenticate(request, username=rut, password=password)
            return render(request, 'login.html', {'form': form, 'error_message': 'RUT no registrado'})
        
        #hay user que corresponda con la contraseña
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            #no corresponde la contraseña al usuario
            form = self.form_class(initial={'rut_body': rut_body, 'rut_dv': rut_dv})
            return render(request, 'login.html', {'form': form, 'error_message': 'Contraseña Equivocada'})
    
    #Este método kickea al usuario del login si está logueado    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

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

class Pedido(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedido.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = DetallePedidoFormSet(self.request.POST, user=self.request.user)  # Pasar user=self.request.user directamente al instanciar el formulario
        else:
            data['formset'] = DetallePedidoFormSet(user=self.request.user)  # Pasar user=self.request.user directamente al instanciar el formulario
        return data
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Agregar request.user a los kwargs del formulario
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                with transaction.atomic():
                    for form in formset:
                        form.instance.pedido = self.object
                        form.save()
        return super().form_valid(form)

DetallePedidoFormSet.formset_js_template_name = 'dynamic_formsets/formset_js.html'

def productos_view(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'planificador/planificador_productos.html', context)

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
        rut_empresa = request.user.empresa.rut_empresa
        clientes = sel_cliente_admin(rut_empresa)
        pedidos_por_mes = cantidad_pedidos_por_mes(rut_empresa)
        rows = []
        for cliente in clientes:
            cliente_dict = {
                'id': cliente['id'],
                'nombre_cliente': cliente['nombre_cliente'],
                'correo_cliente': cliente['correo_cliente'],
                'estado_cliente': cliente['estado_cliente'],
                'cantidad_pedidos': cliente['cantidad_pedidos'],
            }
            rows.append(cliente_dict)
        raw = []
        for pedido in pedidos_por_mes:
            pedidos_dict = {
                'mes': pedido ['mes_texto'],
                'cantidad': pedido ['cantidad']
            }
            raw.append(pedidos_dict)

        return render(request, 'dashboard.html', {'pedidos' : json.dumps(rows), 'pedidosMes' : json.dumps(raw)})

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

def crear_producto(request):
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

def crear_patron_corte(request):
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



 
     
def eliminar_materia_prima(request,id):
    materia_prima=MateriaPrima.objects.get(id=id)
    materia_prima.delete()

    return redirect('plan_materia_prima')