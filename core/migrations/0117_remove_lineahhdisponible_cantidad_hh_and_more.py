# Generated by Django 4.2.4 on 2023-10-30 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0116_demanda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineahhdisponible',
            name='cantidad_hh',
        ),
        migrations.AddField(
            model_name='lineahhdisponible',
            name='dias_produccion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='stockrollizo',
            name='Costo_elab',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='stockrollizo',
            name='dias_produccion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='stockrollizo',
            name='stock_entrante',
            field=models.FloatField(null=True),
        ),

    ]
