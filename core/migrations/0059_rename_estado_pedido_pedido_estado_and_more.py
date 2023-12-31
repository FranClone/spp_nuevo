# Generated by Django 4.1.8 on 2023-07-19 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_rename_grosor_producto_alto_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='estado_pedido',
            new_name='estado',
        ),
        migrations.RenameField(
            model_name='pedido',
            old_name='numero_pedido',
            new_name='producto',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='ancho',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='destino_pedido',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='grosor',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='largo',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='productos_a_producir',
        ),
        migrations.AddField(
            model_name='pedido',
            name='comentario',
            field=models.CharField(default='', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
