# Generated by Django 4.2.4 on 2023-10-17 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0106_stockproducto_producto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallepedido',
            name='cantidad_trozos',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='diametro',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='estado_pedido_linea',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='folio',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='grado_urgencia',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='largo_trozo',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='nota',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='paquetes_saldo',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='paquetes_solicitados',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='piezas_x_cpo',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='piezas_xpaquete',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='piezas_xtrozo',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='separador',
        ),
        migrations.RemoveField(
            model_name='detallepedido',
            name='volumen_obtenido',
        ),
    ]