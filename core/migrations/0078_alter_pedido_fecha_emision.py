# Generated by Django 4.2.4 on 2023-09-08 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_remove_pedido_producto_pedido_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha_emision',
            field=models.DateField(),
        ),
    ]
