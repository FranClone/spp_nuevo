# Generated by Django 4.2.4 on 2023-10-02 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0092_detallepedido_diametro_detallepedido_largo_trozo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='empresa',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='linea',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patroncorte',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='producto',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rollizo',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
    ]
