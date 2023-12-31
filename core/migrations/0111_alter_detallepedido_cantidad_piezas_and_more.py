# Generated by Django 4.2.4 on 2023-10-18 00:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0110_alter_detallepedido_detalle_producto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedido',
            name='cantidad_piezas',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='empaque',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.empaque', verbose_name='Empaque'),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='factura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.factura', verbose_name='Factura'),
        ),
    ]
