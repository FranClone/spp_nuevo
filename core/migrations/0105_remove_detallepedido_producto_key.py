# Generated by Django 4.2.4 on 2023-10-17 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0104_medida_remove_productosempresa_empresa_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallepedido',
            name='producto_key',
        ),
    ]
