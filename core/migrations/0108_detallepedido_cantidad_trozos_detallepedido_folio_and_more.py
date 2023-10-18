# Generated by Django 4.2.4 on 2023-10-18 00:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0107_remove_detallepedido_cantidad_trozos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallepedido',
            name='cantidad_trozos',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='folio',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='grado_urgencia',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='paquetes_saldo',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='paquetes_solicitados',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='piezas_x_cpo',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='piezas_xpaquete',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='piezas_xtrozo',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='volumen_obtenido',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
