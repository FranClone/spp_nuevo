from core.modelos.empresa import Empresa
from core.modelos.cliente_empresa import ClienteEmpresa
from core.modelos.pedido import Pedido
from django.db.models import Count

empresa_oferente = Empresa.objects.get(rut_empresa='10477088-6') # rut de la empresa oferente en cuestión
cliente_empresa = ClienteEmpresa.objects.filter(empresa_oferente=empresa_oferente)
pedidos_por_cliente = Pedido.objects.filter(cliente_empresa__in=cliente_empresa).values('cliente_empresa__empresa_cliente').annotate(total_pedidos=Count('id'))
print(pedidos_por_cliente)