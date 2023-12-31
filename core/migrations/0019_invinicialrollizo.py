# Generated by Django 4.1.7 on 2023-03-28 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_pedido_productos'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvInicialRollizo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_inventario', models.CharField(max_length=300)),
                ('descripcion_inventario', models.CharField(blank=True, max_length=500, null=True)),
                ('diametro', models.IntegerField()),
                ('usuario_crea', models.CharField(blank=True, max_length=20, null=True)),
                ('fecha_crea', models.DateField(auto_now_add=True)),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.bodega', verbose_name='Bodega')),
            ],
            options={
                'db_table': 'INV_INICIAL_ROLLIZO',
            },
        ),
    ]
