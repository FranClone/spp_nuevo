# Generated by Django 4.2.4 on 2023-10-18 00:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0108_detallepedido_cantidad_trozos_detallepedido_folio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedido',
            name='cantidad_trozos',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='paquetes_saldo',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='paquetes_solicitados',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='piezas_x_cpo',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='piezas_xpaquete',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='piezas_xtrozo',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='volumen_obtenido',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
