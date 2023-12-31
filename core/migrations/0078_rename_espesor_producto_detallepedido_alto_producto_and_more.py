# Generated by Django 4.2.4 on 2023-09-21 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_remove_pedido_producto_pedido_producto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detallepedido',
            old_name='espesor_producto',
            new_name='alto_producto',
        ),
        migrations.RenameField(
            model_name='pedido',
            old_name='codigo',
            new_name='orden_pedido',
        ),
  
        migrations.RemoveField(
            model_name='cliente',
            name='estado_cliente',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='fecha_vigencia',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='nombre_fantasia',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='fecha_emision',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='linea_produccion',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='demanda',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='volumen_obtenido',
        ),
        migrations.AddField(
            model_name='cliente',
            name='mercado',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='puerto_destino',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='cantidad_piezas',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='cantidad_trozos',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='paquetes_saldo',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='paquetes_solicitados',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='piezas_xpaquete',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='piezas_xtrozo',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='volumen_obtenido',
            field=models.FloatField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='fecha_produccion',
            field=models.DateField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='version',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='linea',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.linea', verbose_name='Linea'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='nombre_rollizo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.rollizo', verbose_name='Rollizo'),
            preserve_default=False,
        ),

        migrations.AlterField(
            model_name='pedido',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente', verbose_name='Cliente'),
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='producto',
        ),
        migrations.AddField(
            model_name='pedido',
            name='producto',
            field=models.ManyToManyField(through='core.DetallePedido', to='core.producto'),
        ),
    ]
