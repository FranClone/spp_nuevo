# Generated by Django 4.2.4 on 2023-10-14 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0097_detallepedido_producto_key_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockproducto',
            name='producto_key',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
