# Generated by Django 4.2.4 on 2023-09-26 00:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0079_detallepedido_grado_urgencia_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rollizo',
            name='rollizo_largo',
        ),
        migrations.AddField(
            model_name='rollizo',
            name='largo',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='alto_producto',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='ancho_producto',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='cantidad_piezas',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='cantidad_trozos',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='largo_producto',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='paquetes_saldo',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='paquetes_solicitados',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='piezas_xpaquete',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='piezas_xtrozo',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='volumen_obtenido',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='rollizo',
            name='diametro',
            field=models.FloatField(max_length=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.DeleteModel(
            name='RollizoLargo',
        ),
    ]
