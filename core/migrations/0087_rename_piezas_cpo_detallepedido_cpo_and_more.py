# Generated by Django 4.2.5 on 2023-09-27 17:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0086_empaque_factura_detallepedido_banio_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detallepedido',
            old_name='piezas_cpo',
            new_name='cpo',
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='piezas',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
