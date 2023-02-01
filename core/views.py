from django.views.generic import View
from django.shortcuts import render
import pyodbc

#https://www.youtube.com/watch?v=y-goMhYOyts
#está en inglés el video pero se ve bueno
#me compiló ahora y las migraciones se hicieron
#ojalá poder entrar al administrador

#cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=;DATABASE=SPP;UID=sa;PWD=B3t3ch1tda.2021')
#cursor = cnxn.cursor()

#cursor.execute("SELECT * FROM Bodega")

#rows = cursor.fetchall()

#for row in rows:
#    print(row)

#Hay 2 tipos de vistas, clases y funciones esta es de clases
class Administracion(View): #HomeView da acceso a ambos, get req y post req. Get request pide la info para tu ver, post request es lo que envias para que el servidor haga algo con esa información
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'administracion.html', context) #Las '' son el template osea la info en html que se mostrará. También podria definirse context como doble break pero en este caso lo dejamos así, como variable

class Carga_sv(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'carga_servidor.html', context)

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
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'inventario_rollizo.html', context)

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
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'login.html', context)

class Mantenedor(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'mantenedor.html', context)

class Productos(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'productos.html', context)

class Header(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'partials/header.html', context)

#Vistas menu desplegable de header, planificador
class Plan_Bodega(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'planificador/planificador_bodega.html', context)

class Plan_Lineas(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'planificador/planificador_lineas.html', context)

class Plan_Productos(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'planificador/planificador_productos.html', context)

class Plan_Rollizo(View): 
    def get(self, request, *args, **kwargs):
        context={

        }

        return render(request, 'planificador/planificador_rollizo.html', context)