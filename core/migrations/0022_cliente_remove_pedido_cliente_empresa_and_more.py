# Generated by Django 4.1.7 on 2023-04-21 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_clienteempresa_estado_cliente_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('rut_cliente', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre_cliente', models.CharField(max_length=100, verbose_name='Empresa')),
                ('correo_cliente', models.CharField(blank=True, max_length=300, null=True)),
                ('estado_cliente', models.BooleanField(blank=True, null=True)),
                ('fecha_vigencia', models.DateField(blank=True, null=True)),
                ('fecha_crea', models.DateField(auto_now_add=True)),
                ('usuario_crea', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_fantasia', models.CharField(blank=True, max_length=100, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=100, null=True)),
                ('telefono', models.IntegerField(blank=True, null=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresa', to='core.empresa')),
            ],
            options={
                'db_table': 'CLIENTE',
            },
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='cliente_empresa',
        ),
        migrations.DeleteModel(
            name='ClienteEmpresa',
        ),
    ]
