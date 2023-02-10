"""En este módulo se definen todas las vistas para la aplicación web y la lógica para las solicitudes HTTP. 
Maneja las request del usuario y responde con contenido como páginas HTML, JSON, entre otros.
En Django, una vista es una función de Python o basada en clases que toma una web request y devuelve una web response.
Las vistas están típicamente asociadas con una URL en el módulo 'urls.py'.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import JsonResponse
from .models import UserProfile
from .forms import CustomUserCreationForm, LoginForm
from .pedidoForm import PedidoForm
import pyodbc, json, os, datetime, ast

# se intenta conectar a la base de datos
try:
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

#cursor.execute("SELECT * FROM Bodega")

#rows = cursor.fetchall()

#for row in rows:
#    print(row)

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
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_pedido_empresa @rut_empresa=?", os.environ.get('RUT_EMPRESA'))
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        prioridades = ['Alta', 'Media', 'Baja', 'Eliminada']
        return render(request, 'carga_servidor.html', {"rows":rows, "prioridades":prioridades})

class Home(View): 
    """Esta clase define la vista Home"""
    def get(self, request, *args, **kwargs):
        producto_terminado = 1000
        producto_pedido = 5000
        progress = (producto_terminado / producto_pedido)*100
        return render(request, 'home.html', {'progress': progress})

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
        clase_diametrica = list(range(14, 41, 2))
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_rollizo_clasificado_empresa @rut_empresa=?", os.environ.get('RUT_EMPRESA'))
        clas = cursor.fetchall()
        cursor.execute("EXEC dbo.sel_rollizo_empresa @rut_empresa=?", os.environ.get('RUT_EMPRESA'))
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
        #hay user
        try:
            user_profile = UserProfile.objects.get(rut=rut)
            user = user_profile.user
            #corresponde la contraseña al usuario
            if user.check_password(password):
                #entra al sistema
                login(request, user)
                return redirect('home')
            else:
                #no corresponde la contraseña al usuario}
                form = self.form_class()
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid login'})
        #no existe user
        except UserProfile.DoesNotExist:
            form = self.form_class()
            return render(request, 'login.html', {'form': form, 'error_message': 'Invalid login'})
    
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

    def get(self, request):
        form = PedidoForm()
        return render(request, self.template_name, {'form': form})

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
            cursor.execute("{CALL dbo.ins_pedido(?, ?, ?, ?, ?, ?, ?)}", (numero_pedido, destino_pedido, fecha_recepcion, fecha_entrega, os.environ.get('RUT_EMPRESA'), request.user.username, prioridad))
            cursor.commit()
            productos = request.POST.getlist('form-0-producto')
            cantidades = request.POST.getlist('form-0-cantidad')
            for i in range(len(productos)):
                # Ingresa Productos a DETALLE_PEDIDO
                producto_data = ast.literal_eval(productos[i])
                producto_id = producto_data['id']
                producto_nombre = producto_data['nombre']
                cantidad = cantidades[i]
                cursor.execute("{CALL dbo.ins_detalle_pedido(?, ?, ?, ?)}", (producto_id, producto_nombre, cantidad, fecha_entrega))
                cursor.commit()
            return redirect('home')
        return render(request, self.template_name, {'form': form})

class Productos(View): 
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_bodega_empresa @rut_empresa=?", os.environ.get('RUT_EMPRESA'))
        rows = cursor.fetchall()
        cursor.close()
        return render(request, 'productos.html', {"rows":rows})

class Register(View):
    """Esta clase define la vista de Register"""
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data.get('rut')
            UserProfile.objects.create(user=user, rut=rut)
            return redirect('login')
        return render(request, 'register.html', {'form': form})

class Plan_Bodega(View): 
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):        
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_bodega_empresa @rut_empresa=?", os.environ.get('RUT_EMPRESA'))
        rows = cursor.fetchall()
        cursor.close()
        return render(request, 'planificador/planificador_bodega.html', {'rows':rows})

class Plan_Lineas(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_linea_empresa @rut_empresa=?", os.environ.get('RUT_EMPRESA'))
        rows = cursor.fetchall()
        cursor.close()
        return render(request, 'planificador/planificador_lineas.html', {'rows':rows})

class Plan_Productos(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_producto_empresa @rut_empresa=?", os.environ.get('RUT_EMPRESA'))
        rows = cursor.fetchall()
        cursor.close()
        return render(request, 'planificador/planificador_productos.html', {'rows':rows})

class Plan_Rollizo(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_rollizo_empresa @rut_empresa=?", os.environ.get('RUT_EMPRESA'))
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