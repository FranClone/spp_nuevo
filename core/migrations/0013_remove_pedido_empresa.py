# Generated by Django 4.1.7 on 2023-03-28 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_detallepedido_volumen_producto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='empresa',
        ),
    ]
