"""En este script se define la fórmula matemática para poder calcular el porcentaje de progreso de cada uno de los pedidos, considerando
distintos productos y patrones de corte asociados a cada pedido"""

# IMPORTANTE: CONSIDERAR DISTINTOS PRODUCTOS

producto_terminado = 50 # ACÁ ESTÁ CONSIDERADO SOLAMENTE UN PRODUCTO 
producto_pedido = 100

def calcular_porcentaje(producto_terminado, producto_pedido):
    porcentaje = (producto_terminado / producto_pedido) * 100
    print(porcentaje, "%")
    return porcentaje

calcular_porcentaje(producto_terminado, producto_pedido)