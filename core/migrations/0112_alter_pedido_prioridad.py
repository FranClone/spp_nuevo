# Generated by Django 4.2.4 on 2023-10-18 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0111_alter_detallepedido_cantidad_piezas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='prioridad',
            field=models.CharField(blank=True, choices=[('', 'Seleccione una opción'), ('bajo', 'Bajo'), ('mediano', 'Mediano'), ('alto', 'Alto')], default='', max_length=20, null=True),
        ),
    ]
