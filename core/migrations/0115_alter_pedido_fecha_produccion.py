# Generated by Django 4.2.4 on 2023-10-25 14:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0114_alter_pedido_fecha_produccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha_produccion',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
