from datetime import datetime, timedelta
from django.db.models import Q, Max, Sum, F
from .modelos.pedido import Pedido
from .modelos.producto import Producto
from .modelos.empresa import Empresa
from .modelos.detalle_pedido import DetallePedido
from .modelos.rollizo_largo import RollizoLargo
from .modelos.rollizo import Rollizo
from .modelos.bodega import Bodega
from .modelos.linea import Linea

def sel_pedido_empresa(rut_empresa):
    '''Querie para la vista Carga_sv'''
    fecha_actual = datetime.now()
    fecha_inicio = fecha_actual - timedelta(days=30)
    fecha_fin = fecha_actual + timedelta(days=30)
    
    pedidos = Pedido.objects.filter(
        Q(empresa__rut_empresa=rut_empresa) & Q(fecha_recepcion__gte=fecha_inicio) & Q(fecha_entrega__lte=fecha_fin)
    ).all()
    
    return pedidos

def sel_empresa_like(parte_rut):
    '''Seleccionar empresa like'''
    empresas = Empresa.objects.filter(
        Q(rut__startswith=parte_rut) & Q(estado_empresa=1)
    ).values('nombre_empresa')[:5]
    
    return empresas

def sel_pedido_productos_empresa(rut_empresa):
    '''Query para guardar datos en Excel'''
    fecha_actual = datetime.now()
    fecha_inicio = fecha_actual - timedelta(days=30)
    fecha_fin = fecha_actual + timedelta(days=30)
    
    pedidos = Pedido.objects.filter(
        Q(rut_empresa=rut_empresa) & Q(fecha_recepcion__gte=fecha_inicio) & Q(fecha_entrega__lte=fecha_fin)
    ).values('id_pedido', 'detallepedido__detalle_producto', 'detallepedido__volumen_producto')
    
    return pedidos

def insertar_pedido(numero_pedido, destino_pedido, fecha_recepcion, fecha_entrega, rut_empresa, usuario_crea, prioridad):
    pedido = Pedido(numero_pedido=numero_pedido, destino_pedido=destino_pedido, fecha_recepcion=fecha_recepcion, fecha_entrega=fecha_entrega, rut_empresa=rut_empresa, usuario_crea=usuario_crea, prioridad=prioridad)
    pedido.save()

def insertar_detalle_pedido(detalle_producto, volumen_producto, fecha_entrega):
    id_pedido = Pedido.objects.aggregate(Max('id'))['id__max']
    id_producto = Producto.objects.get(nombre_producto=detalle_producto).id
    pedido = Pedido.objects.get(id=id_pedido)
    detalle_pedido = DetallePedido(pedido_id=pedido, producto_id=id_producto, detalle_producto=detalle_producto, volumen_producto=volumen_producto, fecha_entrega=fecha_entrega)
    detalle_pedido.save()

def sel_rollizo_clasificado_empresa(rut_empresa):
    rollizo_largo = RollizoLargo.objects.annotate(
        cantidad=Sum('rollizo__productocorte__producto__stockproducto__cantidad_m3')
    ).filter(
        rollizo__productocorte__producto__stockproducto__bodega__empresa__rut_empresa=rut_empresa
    ).values(
        'id',
        'nombre_largo',
        'largo',
        'cantidad'
    )
    return rollizo_largo

def sel_rollizo_empresa(rut_empresa):
    rollizo_empresa = Rollizo.objects.filter(
        productocorte__producto__stockproducto__bodega__empresa__rut_empresa=rut_empresa
    ).annotate(
        id_linea=F('linea__id'),
        id_largo=F('rollizo_largo__id'),
        nombre_empresa=F('productocorte__producto__stockproducto__bodega__empresa__nombre_empresa'),
        largo=F('rollizo_largo__largo')
    ).values(
        'id',
        'nombre_rollizo',
        'descripcion_rollizo',
        'id_linea',
        'productocorte__producto__stockproducto__bodega__empresa__rut_empresa',
        'diametro',
        'id_largo',
        'usuario_crea',
        'fecha_crea',
        'nombre_empresa',
        'largo'
    )
    return rollizo_empresa

def sel_bodega_empresa(rut_empresa):
    bodegas = Bodega.objects.filter(empresa__rut_empresa=rut_empresa).annotate(
        nombre_empresa=F('empresa__nombre_empresa'),
    ).values(
        'id',
        'empresa__rut_empresa',
        'nombre_bodega',
        'descripcion_bodega',
        'usuario_crea',
        'fecha_crea',
        'nombre_empresa'
    )
    return bodegas

def sel_linea_empresa(rut_empresa):
    lineas = Linea.objects.filter(rollizo__productocorte__producto__stockproducto__bodega__empresa__rut_empresa=rut_empresa)\
                .annotate(nombre_empresa=F('rollizo__productocorte__producto__stockproducto__bodega__empresa__nombre_empresa'))\
                .annotate(rut_empresa=F('rollizo__productocorte__producto__stockproducto__bodega__empresa__rut_empresa'))\
                .values('id', 'rut_empresa', 'nombre_linea', 'descripcion_linea', 'usuario_crea', 'fecha_crea', 'nombre_empresa')
    return lineas

def sel_producto_empresa(rut_empresa):
    queryset = Producto.objects.filter(empresa__rut_empresa=rut_empresa).annotate(nombre_empresa=F('empresa__nombre_empresa'))
    return queryset