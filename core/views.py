"""En este módulo se definen todas las vistas para la aplicación web y la lógica para las solicitudes HTTP. 
Maneja las request del usuario y responde con contenido como páginas HTML, JSON, entre otros.
En Django, una vista es una función de Python o basada en clases que toma una web request y devuelve una web response.
Las vistas están típicamente asociadas con una URL en el módulo 'urls.py'.
"""

from axes.decorators import axes_dispatch
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.base import ContextMixin
from django.http import JsonResponse, FileResponse, Http404
from .models import UserProfile
from .forms import CustomUserCreationForm, LoginForm
from .pedidoForm import PedidoForm
import pyodbc, json, os, datetime, openpyxl, bleach

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
        context={

        }
        return render(request, 'administracion.html', context) 

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
        # se crea un cursor de la base de datos
        cursor = conexion.cursor()
        # se llama al procedimiento almacenado
        rut_empresa = request.user.userprofile.rut_empresa
        cursor.execute("EXEC dbo.sel_pedido_empresa @rut_empresa=?", [rut_empresa])
        # se guardan los datos del pedido
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        prioridades = ['Alta', 'Media', 'Baja', 'Eliminada']
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
    cursor = conexion.cursor()
    cursor.execute("EXEC dbo.sel_empresa_like @parte_rut=?", parte_rut)
    empresas = [row.nombre_empresa for row in cursor.fetchall()]
    cursor.close()
    return JsonResponse({'empresas': empresas})

class Home(View): 
    """Esta clase define la vista Home"""
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        #cálculo progress
        producto_terminado = 1000
        producto_pedido = 5000
        progress = (producto_terminado / producto_pedido)*100
        cursor = conexion.cursor()
        rut_empresa = request.user.userprofile.rut_empresa
        #buscamos pedidos en base de datos
        cursor.execute("EXEC dbo.sel_pedido_empresa @rut_empresa=?", [rut_empresa])
        #obtenemos datos
        rows = cursor.fetchall()
        #datos para guardarlos en un diccionarios
        column_names = [column[0] for column in cursor.description]
        #método para convertir en diccionario compatible con JS para parsear en JSON
        def convert_to_dict(data):
            result = []
            for row in data:
                row_dict = {}
                for i, value in enumerate(row):
                    if value is None:
                        #transformamos None a "null", ya que None no existe en JavaScript
                        value = "null"
                    #guardamos valores en diccionario
                    row_dict[column_names[i]] = value
                #agregamos valores a diccionario
                result.append(row_dict)
            return result
        #aplicamos función
        result = convert_to_dict(rows)
        #en este for loop agregamos la duración de cada producto usando las fechas
        cursor.execute("EXEC dbo.sel_pedido_productos_empresa @rut_empresa=?", [rut_empresa])
        #obtenemos todo el resultado
        detalle = cursor.fetchall()
        #obtiene los nombres de las columnas
        column_names = [column[0] for column in cursor.description]
        #convierte a diccionario, usando el anterior
        detalle = convert_to_dict(detalle)
        cursor.close()
        for item in result:
            #agrega un atributo de duración al diccionario
            fecha_entrega = item.get("fecha_entrega")
            fecha_recepcion = item.get("fecha_recepcion")
            if fecha_entrega and fecha_recepcion:
                fecha_entrega = datetime.datetime.strptime(fecha_entrega, "%Y-%m-%d")
                fecha_recepcion = datetime.datetime.strptime(fecha_recepcion, "%Y-%m-%d")
                delta = fecha_entrega - fecha_recepcion
                #asignación a la duración
                item["duration"] = delta.days
                item["producto"] = []
                item["cantidad"] = []
            #obtiene los productos, con su respectiva cantidad, al diccionario
            for value in detalle:
                if item.get("id_pedido") == value.get("id_pedido"):
                    item["producto"].append(value.get("detalle_producto"))
                    item["cantidad"].append(value.get("volumen_producto"))
                    

        #convertimos a json para que pueda ser leído por JS
        result = json.dumps(result)
        return render(request, 'home.html', {'progress': progress, 'result': result})
    
    @method_decorator(login_required) 
    def post(self, request, *args, **kwargs):
        #Carga Archivo
        try:
            archivo = request.FILES['carga-masiva']
        except:
            return redirect('home')

        # Verifica el tamaño del archivo
        if archivo.size > 100000000:  # 100 MB
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
        rut_empresa = request.user.userprofile.rut_empresa

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
                cursor = conexion.cursor()
                cursor.execute("{CALL dbo.ins_pedido(?, ?, ?, ?, ?, ?, ?)}", (numero_pedido, destino_pedido, fecha_recepcion, fecha_entrega, rut_empresa, request.user.username, prioridad))
                cursor.commit()
                cursor.close()
            # Si las dos últimas columnas están llenas, guardamos los valores en la base de datos utilizando
            if fila[5] and fila[6] != 'None':
                producto_nombre = fila[5]
                cantidad = fila[6]
                cursor.execute("{CALL dbo.ins_detalle_pedido(?, ?, ?)}", (producto_nombre, cantidad, fecha_entrega))
                cursor.commit()  
                cursor.close()
            
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
        cursor = conexion.cursor()
        rut_empresa = request.user.userprofile.rut_empresa
        cursor.execute("EXEC dbo.sel_rollizo_clasificado_empresa @rut_empresa=?", [rut_empresa])
        clas = cursor.fetchall()
        cursor.execute("EXEC dbo.sel_rollizo_empresa @rut_empresa=?", [rut_empresa])
        noclas = cursor.fetchall()
        cursor.close()
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
    """Esta clase define la vista de Login"""
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
            username = user_profile.user.username
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

class Pedido(View):
    template_name = 'pedido.html'

    @method_decorator(login_required)
    def get(self, request):
        form = PedidoForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = PedidoForm(request.POST)
        if form.is_valid():
            cursor = conexion.cursor()
            numero_pedido = form.cleaned_data['numero_pedido']
            fecha_recepcion = form.cleaned_data['fecha_recepcion']
            fecha_recepcion = datetime.datetime.combine(fecha_recepcion, datetime.time.min)
            fecha_entrega = form.cleaned_data['fecha_entrega']
            fecha_entrega = datetime.datetime.combine(fecha_entrega, datetime.time.min)
            destino_pedido = form.cleaned_data['destino_pedido']
            # id_bodega = form.cleaned_data['nombre_bodega']
            prioridad = form.cleaned_data['prioridad']
            # Ingresa Datos a Pedido
            rut_empresa = request.user.userprofile.rut_empresa
            cursor.execute("{CALL dbo.ins_pedido(?, ?, ?, ?, ?, ?, ?)}", (numero_pedido, destino_pedido, fecha_recepcion, fecha_entrega, rut_empresa, request.user.username, prioridad))
            cursor.commit()
            productos = request.POST.getlist('form-0-producto')
            cantidades = request.POST.getlist('form-0-cantidad')
            for i in range(len(productos)):
                # Ingresa Productos a DETALLE_PEDIDO
                producto_nombre = productos[i]
                cantidad = cantidades[i]
                cursor.execute("{CALL dbo.ins_detalle_pedido(?, ?, ?)}", (producto_nombre, cantidad, fecha_entrega))
                cursor.commit()
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class Pedido_Multiple(View):
    template_name = 'pedido_multiple.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = PedidoForm()
        return render(request, self.template_name, {'form': form})

class Productos(View): 
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        rut_empresa = request.user.userprofile.rut_empresa
        cursor.execute("EXEC dbo.sel_bodega_empresa @rut_empresa=?", [rut_empresa])
        rows = cursor.fetchall()
        cursor.close()
        return render(request, 'productos.html', {"rows":rows})

class Register(View):
    """Esta clase define la vista de Register"""
    def get(self, request):
        form = CustomUserCreationForm()
        cursor = conexion.cursor()
        parte_rut = 7
        cursor.execute("EXEC dbo.sel_empresa_like @parte_rut=?", parte_rut)
        row = cursor.fetchone()
        cursor.close()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data.get('rut')
            rut_empresa = form.cleaned_data.get('rut_empresa')
            UserProfile.objects.create(user=user, rut=rut, rut_empresa=rut_empresa)
            return redirect('login')
        return render(request, 'register.html', {'form': form})

class Plan_Bodega(View): 
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):        
        cursor = conexion.cursor()
        rut_empresa = request.user.userprofile.rut_empresa
        cursor.execute("EXEC dbo.sel_bodega_empresa @rut_empresa=?", [rut_empresa])
        rows = cursor.fetchall()
        cursor.close()
        return render(request, 'planificador/planificador_bodega.html', {'rows':rows})

class Plan_Lineas(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        rut_empresa = request.user.userprofile.rut_empresa
        cursor.execute("EXEC dbo.sel_linea_empresa @rut_empresa=?", [rut_empresa])
        rows = cursor.fetchall()
        cursor.close()
        return render(request, 'planificador/planificador_lineas.html', {'rows':rows})

class Plan_Productos(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        rut_empresa = request.user.userprofile.rut_empresa
        cursor.execute("EXEC dbo.sel_producto_empresa @rut_empresa=?", [rut_empresa])
        rows = cursor.fetchall()
        cursor.close()
        return render(request, 'planificador/planificador_productos.html', {'rows':rows})

class Plan_Rollizo(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        rut_empresa = request.user.userprofile.rut_empresa
        cursor.execute("EXEC dbo.sel_rollizo_empresa @rut_empresa=?", [rut_empresa])
        rows = cursor.fetchall()
        cursor.close()
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