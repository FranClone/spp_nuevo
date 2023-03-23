from datetime import datetime, timedelta
from django.db.models import Q, Max, Sum, F
from .modelos.pedido import Pedido
from .modelos.producto import Producto
from .modelos.empresa import Empresa
from .modelos.detalle_pedido import DetallePedido
from .modelos.rollizo_largo import RollizoLargo
from .modelos.rollizo import Rollizo

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
        cantidad=Sum('rollizo__stock_rollizo__producto_corte__producto__stock_producto__cantidad')
    ).annotate(
        nombre_largo=F('nombre_largo'),
        largo=F('largo'),
        id_largo=F('largo_id')
    ).filter(
        rollizo__stock_rollizo__producto_corte__producto__stock_producto__bodega__empresa__rut_empresa=rut_empresa
    ).values(
        'largo_id',
        'nombre_largo',
        'largo',
        'cantidad'
    )
    return rollizo_largo

def sel_rollizo_empresa(rut_empresa):
    rollizo_empresa = Rollizo.objects.filter(
        stock_rollizo__producto_corte__producto__stock_producto__bodega__empresa__rut_empresa=rut_empresa
    ).annotate(
        id_linea=F('id_linea__id_linea'),
        id_largo=F('id_largo__id_largo'),
        usuario_crea=F('usuario_crea__username'),
        fecha_crea=F('fecha_crea__date'),
        nombre_empresa=F('stock_rollizo__producto_corte__producto__stock_producto__bodega__empresa__nombre_empresa'),
        largo=F('id_largo__largo')
    ).values(
        'id_rollizo',
        'nombre_rollizo',
        'descripcion_rollizo',
        'id_linea',
        'stock_rollizo__producto_corte__producto__stock_producto__bodega__empresa__rut_empresa',
        'diametro',
        'id_largo',
        'usuario_crea',
        'fecha_crea',
        'nombre_empresa',
        'largo'
    )
    return rollizo_empresa