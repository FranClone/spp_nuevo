from datetime import datetime, timedelta
from django.db.models import Q, Max, Sum, F, Count, IntegerField, CharField, Case, When, Value
from django.db.models.functions import TruncMonth, Cast, ExtractMonth
from django.db.models import Count
from .modelos.cliente import Cliente
from .modelos.pedido import Pedido
from .modelos.producto import Producto
from .modelos.empresa import Empresa
from .modelos.inv_inicial_rollizo import InvInicialRollizo
from .modelos.detalle_pedido import DetallePedido
from .modelos.rollizo_largo import RollizoLargo
from .modelos.rollizo import Rollizo
from .modelos.bodega import Bodega
from .modelos.linea import Linea



def sel_cliente_admin(rut_empresa):
    '''Querie para la vista Administración'''
    clientes = Cliente.objects.filter(empresa__rut_empresa=rut_empresa
                                      ).annotate(cantidad_pedidos=Count('pedido'),
                                                 ).values('id', 'nombre_cliente', 'correo_cliente', 'estado_cliente', 'cantidad_pedidos')
    return clientes

def cantidad_pedidos_por_mes(rut_empresa):
    seis_meses_atras = datetime.now() - timedelta(days=180)

    meses = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre'
    }

    pedidos_por_mes = Pedido.objects.filter(
        cliente__empresa__rut_empresa=rut_empresa,
        fecha_recepcion__gte=seis_meses_atras
    ).annotate(
        mes=TruncMonth('fecha_recepcion'),
        mes_numero=ExtractMonth('fecha_recepcion')
    ).annotate(
        mes_texto=Value('', output_field=CharField())
    ).values(
        'mes',
        'mes_numero',
        'mes_texto'
    ).annotate(
        cantidad=Count('id', output_field=IntegerField())
    ).order_by(
        'mes'
    )

    for item in pedidos_por_mes:
        item['mes_texto'] = meses[item['mes_numero']]

    return pedidos_por_mes

def sel_pedido_empresa(rut_empresa):
    '''Querie para la vista Carga_sv'''
    fecha_actual = datetime.now()
    fecha_inicio = fecha_actual - timedelta(days=30)
    fecha_fin = fecha_actual + timedelta(days=30)

    pedidos = Pedido.objects.filter(
        Q(cliente__empresa__rut_empresa=rut_empresa) & Q(
            fecha_recepcion__gte=fecha_inicio) & Q(fecha_entrega__lte=fecha_fin)
    ).annotate(nombre_cliente=F('cliente__nombre_cliente')
               ).values('id', 'nombre_cliente', 'numero_pedido', 'destino_pedido', 'fecha_recepcion', 'fecha_entrega', 'prioridad')

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
        Q(cliente__empresa__rut_empresa=rut_empresa) & Q(
            fecha_recepcion__gte=fecha_inicio) & Q(fecha_entrega__lte=fecha_fin)
    ).annotate(detalle_producto=F('detallepedido__detalle_producto'),
               volumen_producto=F('detallepedido__volumen_producto'),
               nombre_producto=F('detallepedido__producto__nombre_producto')
               ).values('id', 'numero_pedido', 'detalle_producto', 'volumen_producto', 'nombre_producto')

    return pedidos


def insertar_pedido(numero_pedido, destino_pedido, fecha_recepcion, fecha_entrega, rut_empresa_oferente, rut_empresa_cliente, usuario_crea, prioridad):
    # Buscar las empresas por su rut
    empresa_oferente = Empresa.objects.get(rut_empresa=rut_empresa_oferente)

    # Crear un nuevo ClienteEmpresa
    cliente_empresa = Cliente.objects.create(
        rut_cliente=rut_empresa_cliente,
        empresa=empresa_oferente,
        usuario_crea=usuario_crea
    )

    # Crear un nuevo Pedido
    pedido = Pedido.objects.create(
        numero_pedido=numero_pedido,
        destino_pedido=destino_pedido,
        fecha_recepcion=fecha_recepcion,
        fecha_entrega=fecha_entrega,
        usuario_crea=usuario_crea,
        prioridad=prioridad,
        cliente_empresa=cliente_empresa
    )


def insertar_detalle_pedido(detalle_producto, volumen_producto, fecha_entrega):
    id_pedido = Pedido.objects.aggregate(Max('id'))['id__max']
    id_producto = Producto.objects.get(nombre_producto=detalle_producto).id
    pedido = Pedido.objects.get(id=id_pedido)
    detalle_pedido = DetallePedido(pedido_id=pedido, producto_id=id_producto, detalle_producto=detalle_producto,
                                   volumen_producto=volumen_producto, fecha_entrega=fecha_entrega)
    detalle_pedido.save()


def sel_rollizo_clasificado_empresa(rut_empresa):
    rollizo_largo = RollizoLargo.objects.annotate(
        cantidad=Sum(
            'rollizo__productocorte__producto__stockproducto__cantidad_m3')
    ).filter(
        rollizo__productocorte__producto__productosempresa__empresa__rut_empresa=rut_empresa
    ).annotate(rollizo_id=F('rollizo__id'),
               descripcion_rollizo=F('rollizo__descripcion_rollizo'),
               linea_id=F('rollizo__linea__id'),
               diametro=F('rollizo__diametro')
               ).values(
        'rollizo_id',
        'descripcion_rollizo',
        'linea_id',
        'diametro',
        'nombre_largo',
        'largo',
        'cantidad'
    )
    return rollizo_largo


def sel_rollizo_empresa(rut_empresa):
    rollizo_empresa = InvInicialRollizo.objects.filter(
        bodega__empresa__rut_empresa=rut_empresa
    ).values(
        'id',
        'nombre_inventario',
        'descripcion_inventario',
        'diametro',
        'cant_m3'
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
    queryset = Producto.objects.filter(empresa__rut_empresa=rut_empresa).annotate(
        nombre_empresa=F('empresa__nombre_empresa'))
    return queryset


def sel_cliente(rut_empresa):
    # rut de la empresa oferente en cuestión
    empresa_oferente = Empresa.objects.get(rut_empresa=rut_empresa)
    cliente_empresa = Cliente.objects.filter(empresa=empresa_oferente)
    pedidos_por_cliente = Pedido.objects.filter(cliente_empresa__in=cliente_empresa).values(
        'cliente_empresa__empresa_cliente').annotate(total_pedidos=Count('rut_empresa'))

    return pedidos_por_cliente

