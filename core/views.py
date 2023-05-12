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
from .forms import CustomUserCreationForm, LoginForm
from .modelos.pedido import Pedido
from .pedidoForm import PedidoForm
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

def superuser_required(view_func):
    """Restrict a view to superusers only"""
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

def staff_required(view_func):
    """Restrict a view to staff members only"""
    decorated_view_func = user_passes_test(lambda u: u.is_staff)(view_func)
    return decorated_view_func

def aserradero_required(function=None):
    """
    Decorador que verifica si el usuario es del aserradero o es superusuario.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.groups.filter(name='aserradero').exists()),
        login_url='/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def cliente_required(function=None):
    """
    Decorador que verifica si el usuario es del aserradero, el cliente o es superusuario.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.groups.filter(name='aserradero').exists() or u.groups.filter(name='cliente').exists()),
        login_url='/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

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
        empresas = sel_empresa_like(parte_rut)
    return JsonResponse({'empresas': empresas})

class Home(View): 
    """Esta clase define la vista Home"""
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        #cálculo progress
        producto_terminado = 1000
        producto_pedido = 5000
        progress = (producto_terminado / producto_pedido)*100
        rut_empresa = request.user.empresa.rut_empresa
        #obtenemos datos
        pedidos = sel_pedido_empresa(rut_empresa)
        #datos para guardarlos en un diccionarios
        # Convertir los objetos de pedido a un diccionario
        pedidos_list = []
        for pedido in pedidos:
            pedido_dict = {}
            for key, value in pedido.items():
                if isinstance(value, (datetime.date, datetime.datetime)):
                    pedido_dict[key] = value.isoformat()
                else:
                    pedido_dict[key] = value
            pedidos_list.append(pedido_dict)
        pedidos_json = json.dumps(pedidos_list)
        productos = sel_pedido_productos_empresa(rut_empresa)
        productos_dict = [pedido for pedido in productos]
        # Convertir el diccionario a formato JSON
        productos_json = json.dumps(productos_dict)
        
        return render(request, 'home.html', {'progress': progress, 'pedidos': pedidos_json, 'productos': productos_json})
    
    @method_decorator(login_required) 
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

        #Retorna archivo en formato Workbook
        wb = openpyxl.load_workbook(archivo)
        #Obtiene la página que se obtiene al inicio
        hoja = wb.active
        #Itera sobre la hoja
        numero_pedido = None
        fecha_recepcion = None
        fecha_entrega = None
        destino_pedido = None
        prioridad = None
        rut_empresa = request.user.empresa.rut_empresa
        rut = request.user.rut

        for i, fila in enumerate(hoja.iter_rows(values_only=True)):
            # Salta la primera fila
            if i == 0:
                continue
            # Sanitiza los datos en la fila
            fila = [bleach.clean(str(x), tags=[], strip=True) for x in fila]
            # Si las 5 primeras columnas están llenas, guardamos los valores en las variables correspondientes
            if fila[0] and fila[1] and fila[2] and fila[3] and fila[4] != 'None':
                numero_pedido = fila[0]
                fecha_recepcion = fila[1]
                fecha_entrega = fila[2]
                destino_pedido = fila[3]
                prioridad = fila[4]
                insertar_pedido(numero_pedido, destino_pedido ,fecha_recepcion, fecha_entrega, rut_empresa, rut, prioridad)
            # Si las dos últimas columnas están llenas, guardamos los valores en la base de datos utilizando
            if fila[5] and fila[6] != 'None':
                producto_nombre = fila[5]
                cantidad = fila[6]
                insertar_detalle_pedido(producto_nombre, cantidad, fecha_entrega)
            
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

class Inventario_roll_nc(View):
    """Esta clase define la vista de Inventario"""
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'inventario_rollizo_nc.html', context) 

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

# Esta vista es para crear un nuevo pedido y sus detalles relacionados
class Pedido(CreateView):
    # El modelo que se usará para crear un nuevo pedido
    model = Pedido
    # El formulario que se usará para ingresar los datos del pedido
    form_class = PedidoForm
    # El éxito URL a donde se dirigirá al usuario después de crear el pedido
    success_url = reverse_lazy('home')
    # El nombre de la plantilla HTML que se usará para mostrar la página de creación de pedido
    template_name = 'pedido.html'

    # Este método se utiliza para obtener los datos necesarios para renderizar la plantilla
    def get_context_data(self, **kwargs):
        # Obtener los datos de contexto que se proporcionan por la superclase
        data = super().get_context_data(**kwargs)
        # Si la solicitud es un POST, entonces se recibieron datos del formulario
        if self.request.POST:
            # Crea un formulario en línea para ingresar los detalles del pedido
            # y asocia el formulario en línea con los datos recibidos del formulario de pedido principal
            data['detalles'] = DetallePedidoInlineFormSet(self.request.POST)
        else:
            # Si la solicitud no es un POST, entonces no hay datos para el formulario en línea
            # Así que se crea un formulario en línea vacío
            data['detalles'] = DetallePedidoInlineFormSet()
        return data

    # Este método se llama cuando el formulario es válido
    def form_valid(self, form):
        # Obtener los datos de contexto necesarios para guardar los detalles del pedido
        context = self.get_context_data()
        detalles = context['detalles']
        # Utiliza una transacción de la base de datos para guardar el pedido y sus detalles relacionados
        with transaction.atomic():
            # Asigna el usuario actual como el creador del pedido
            form.instance.creado_por = self.request.user
            # Guarda el pedido principal
            self.object = form.save()
            # Si el formulario en línea es válido, asocia los detalles del pedido con el pedido principal
            if detalles.is_valid():
                # Asigna el pedido principal como la instancia de los detalles del pedido
                detalles.instance = self.object
                # Guarda los detalles del pedido relacionados con el pedido principal
                detalles.save()
        # Retorna la respuesta HTTP para indicar que el formulario fue validado correctamente
        return super().form_valid(form)

class Pedido_Multiple(View):
    template_name = 'pedido_multiple.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = PedidoForm(request=request)
        return render(request, self.template_name, {'form': form})

class Productos(View): 
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        rut_empresa = request.user.empresa.rut_empresa
        rows = sel_bodega_empresa(rut_empresa)
        return render(request, 'productos.html', {"rows":rows})

class Register(View):
    def get(self, request):
        form = CustomUserCreationForm()
        
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data.get('rut')
            rut_empresa = form.cleaned_data.get('rut_empresa')
            UserProfile.objects.create(user=user, rut=rut, rut_empresa=rut_empresa.rut_empresa)
            return redirect('login')
        return render(request, 'register.html', {'form': form})

class Plan_Bodega(View): 
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):        
        rut_empresa = request.user.empresa.rut_empresa
        rows = sel_bodega_empresa(rut_empresa)
        return render(request, 'planificador/planificador_bodega.html', {'rows':rows})

class Plan_Lineas(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        rut_empresa = request.user.empresa.rut_empresa
        rows = sel_linea_empresa(rut_empresa)
        return render(request, 'planificador/planificador_lineas.html', {'rows':rows})

class Plan_Productos(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        rut_empresa = request.user.empresa.rut_empresa
        rows = sel_producto_empresa(rut_empresa)
        return render(request, 'planificador/planificador_productos.html', {'rows':rows})

class Plan_Rollizo(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        rut_empresa = request.user.empresa.rut_empresa
        rows = sel_rollizo_clasificado_empresa(rut_empresa)
        return render(request, 'planificador/planificador_rollizo.html', {'rows':rows})

def get_data(request):
    """Esta función asigna los valores a cada barra del bar chart"""
    P1 = 100
    P2 = 77
    P3 = 89
    P4 = 87
    P5 = 100
    data = {
        'labels': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'datasets': [
            {
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 1,
                'data': [P1, P2, P3, P4, P5]
            }
        ]
    }
    return JsonResponse(data)

def my_view(request):
    # crea una variable de progreso y la envía a 'home.html'
    progress = 0
    return render(request, 'home.html', {'progress': progress})

class Dashboard(View): 
    """Esta clase define la vista Dashboard"""
    @method_decorator(login_required) #HomeView da acceso a ambos, get req y post req. Get request pide la info para tu ver, post request es lo que envias para que el servidor haga algo con esa información
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
        print(pedidos_por_mes)
        return render(request, 'dashboard.html', {'pedidos' : json.dumps(rows)})
    
    # def get(request):
    #     cantPedidoMes = sel_pedidos_por_mes()
    #     meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    #     cantidad_pedidos = [dato['cantidad'] for dato in cantPedidoMes]
    #     datos_cantPedidos = json.dumps({'meses': meses, 'cantidad_pedidos': cantidad_pedidos})

    #     return render(request, 'dashboard.html', {'cantidad pedidos': datos_cantPedidos})  
