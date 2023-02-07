from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View
from .models import UserProfile
from .forms import CustomUserCreationForm, LoginForm
import pyodbc, json

#https://www.youtube.com/watch?v=y-goMhYOyts
#está en inglés el video pero se ve bueno
#me compiló ahora y las migraciones se hicieron
#ojalá poder entrar al administrador
try:
    conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.100.138,1434;DATABASE=SPP;UID=sa;PWD=B3t3ch1tda.2021')
    print("conexión a base de datos exitosa")

except Exception as ex:
    print(ex)

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
        return render(request, 'administracion.html', context) #Las '' son el template osea la info en html que se mostrará. También podria definirse context como doble break pero en este caso lo dejamos así, como variable

class Bar_chart(View):
    @method_decorator(login_required) #HomeView da acceso a ambos, get req y post req. Get request pide la info para tu ver, post request es lo que envias para que el servidor haga algo con esa información
    def get(self, request, *args, **kwargs):
        """Cálculo matemático para obtener la producción global del aserradero en porcentaje"""

        # si me pidieron 1000 m^3 de producto_1 y hasta el día de hoy llevo 500 m^3 de producto_1
        mcubicos_pedido_producto_1 = [4000, 5000, 6000, 7000, 8000]
        mcubicos_cortados_producto_1 = [2000, 3000, 2500, 2000, 4000]
        produccion_global = []
        for i in range(len(mcubicos_pedido_producto_1)):
            produccion_global.append((mcubicos_cortados_producto_1[i] / mcubicos_pedido_producto_1[i]) * 100)
        return render(request, 'bar_chart.html', {"pr_global":json.dumps(produccion_global)})


class Carga_sv(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_pedido_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        return render(request, 'carga_servidor.html', {"rows":rows})

class Home(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'home.html', context)

class Index(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'index.html', context)

class Inventario_pdto(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'inventario_producto.html', context)

class Inventario_roll(View):
    @method_decorator(login_required) 
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
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'inventario_rollizo_nc.html', context) 

class Lista_pedidos(View): 
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
        rut = request.POST['rut']
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
                #no corresponde la contraseña al usuario
                return render(request, 'login.html', {'error_message': 'Invalid login'})
        #no existe user
        except UserProfile.DoesNotExist:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    
    #Este método kickea al usuario del login si está logueado    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Home')
        return super().dispatch(request, *args, **kwargs)

class Logout(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class Mantenedor(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'mantenedor.html', context)

class Productos(View): 
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_bodega_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
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
            UserProfile.objects.create(user=user, rut=rut)
            return redirect('login')
        return render(request, 'register.html', {'form': form})

#Vistas menu desplegable de header, planificador

class Plan_Bodega(View): 
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):        
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_bodega_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        return render(request, 'planificador/planificador_bodega.html', {'rows':rows})

class Plan_Lineas(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_linea_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        return render(request, 'planificador/planificador_lineas.html', {'rows':rows})

class Plan_Productos(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_producto_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        return render(request, 'planificador/planificador_productos.html', {'rows':rows})

class Plan_Rollizo(View):
    @method_decorator(login_required) 
    def get(self, request, *args, **kwargs):
        cursor = conexion.cursor()
        cursor.execute("EXEC dbo.sel_rollizo_empresa @rut_empresa=?", "77003725-5")
        rows = cursor.fetchall()
        cursor.commit()
        cursor.close()
        return render(request, 'planificador/planificador_rollizo.html', {'rows':rows})