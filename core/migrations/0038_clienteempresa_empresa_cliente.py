# Generated by Django 4.1.7 on 2023-04-21 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_pedido_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.empresa')),
            ],
            options={
                'db_table': 'CLIENTE_EMPRESA',
            },
        ),
        migrations.AddField(
            model_name='empresa',
            name='cliente',
            field=models.ManyToManyField(through='core.ClienteEmpresa', to='core.cliente'),
        ),
    ]
