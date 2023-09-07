 #resources.py  from import_export import resources  
from import_export import resources
from .producto import Producto
 
class ProductoResource(resources.ModelResource):  
   class Meta:  
     model = Producto  
     fields = [
        'codigo',
        'nombre',
        'descripcion',
        'largo',
        'ancho',
        'alto',
        'demanda',
        'inventario_inicial',
        'valor_inventario',
        'costo_almacenamiento',
        'volumen_obtenido',
        'inventario_final',
            
        ]
     