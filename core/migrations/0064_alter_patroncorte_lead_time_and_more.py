# Generated by Django 4.2.4 on 2023-08-24 16:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_alter_pedido_comentario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patroncorte',
            name='lead_time',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='patroncorte',
            name='rendimiento',
            field=models.FloatField(max_length=5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AlterField(
            model_name='patroncorte',
            name='setup_time',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='patroncorte',
            name='velocidad_linea',
            field=models.FloatField(),
        ),
    ]
