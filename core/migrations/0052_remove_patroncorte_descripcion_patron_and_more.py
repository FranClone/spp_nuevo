# Generated by Django 4.1.8 on 2023-06-22 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_alter_producto_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patroncorte',
            name='descripcion_patron',
        ),
        migrations.RemoveField(
            model_name='patroncorte',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='patroncorte',
            name='fecha_crea',
        ),
        migrations.RemoveField(
            model_name='patroncorte',
            name='usuario_crea',
        ),
        migrations.AddField(
            model_name='patroncorte',
            name='clase_diametrica_rollizo',
            field=models.CharField(default='Valor predeterminado', max_length=20),
        ),
        migrations.AddField(
            model_name='patroncorte',
            name='codigo_patron',
            field=models.CharField(default='Valor predeterminado', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='patroncorte',
            name='nombre_patron',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterModelTable(
            name='patroncorte',
            table=None,
        ),
    ]
