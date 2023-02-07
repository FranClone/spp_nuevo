"""En este módulo se definen todas las vistas para la aplicación web y la lógica para las solicitudes HTTP. 
Maneja las request del usuario y responde con contenido como páginas HTML, JSON, entre otros.
En Django, una vista es una función de Python o basada en clases que toma una web request y devuelve una web response.
Las vistas están típicamente asociadas con una URL en el módulo 'urls.py'.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import JsonResponse
from .models import UserProfile
from .forms import CustomUserCreationForm, LoginForm
import pyodbc, json

# se intenta conectar a la base de datos
try:
    conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.100.138,1434;DATABASE=SPP;UID=sa;PWD=B3t3ch1tda.2021')
    print("conexión a base de datos exitosa")

except Exception as ex:
    print(ex)

class Administracion(View): 
    """Esta clase define la vista de Administración"""
    def get(self, request, *args, **kwargs):
        context={

        }
        return render(request, 'administracion.html', context) 

class Bar_chart(View): 
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
    """Esta clase define la vista de Carga"""
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_pedido_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        return render(request, 'carga_servidor.html', {"rows":rows})

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
    """Esta clase define la vista de Inventario"""
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_rollizo_largo_empresa @rut_empresa=?", "77003725-5")
        clas = cursor.fetchall()
        cursor.execute("EXEC dbo.sel_rollizo_empresa @rut_empresa=?", "77003725-5")
        noclas = cursor.fetchall()
        cursor.commit()
        cursor.close()
        return render(request, 'inventario_rollizo.html', {"clas":clas, "noclas":noclas})

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
    template_name = 'login.html'
    success_url = '/home/'
    
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

    def post(self, request):
        rut = request.POST['rut']
        password = request.POST['password']
        try:
            user_profile = UserProfile.objects.get(rut=rut)
            user = user_profile.user
            if user.check_password(password):
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid login'})
        except UserProfile.DoesNotExist:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
        
    def form_valid(self, form):
        rut = form.cleaned_data.get('rut')
        password = form.cleaned_data.get('password')

        user = authenticate(username=rut, password=password)

        if user:
            if user.is_active:
                login(self.request, user)
                return redirect(self.success_url)
            else:
                messages.error(self.request, "Tu cuenta esta desactivada")
                return redirect('login')
        else:
            messages.error(self.request, "Invalid Login")
            return redirect('login')
        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.path != reverse('login'):
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

"""Este método decorativo autentica a un usuario para validar y permitir acceso a las vistas"""
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

class Mantenedor(View): 
    """Esta clase define la vista de Mantenedor"""
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'mantenedor.html', context)

class Productos(View): 
    """Esta clase define la vista de Productos"""
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_bodega_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
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
    """Esta clase define la vista de Planificador Bodega"""
    def get(self, request, *args, **kwargs):        
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_bodega_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        return render(request, 'planificador/planificador_bodega.html', {'rows':rows})

class Plan_Lineas(View): 
    """Esta clase define la vista de Planificador de Lineas"""
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_linea_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        return render(request, 'planificador/planificador_lineas.html', {'rows':rows})

class Plan_Productos(View): 
    """Esta clase define la vista de Planificador de Productos"""
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_producto_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        return render(request, 'planificador/planificador_productos.html', {'rows':rows})

class Plan_Rollizo(View): 
    """Esta clase define la vista de Planificador de Rollizos"""
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_rollizo_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
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