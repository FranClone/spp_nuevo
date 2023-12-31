# Generated by Django 4.2.4 on 2023-10-17 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0102_remove_rollizo_linea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empresa',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='empresa',
            name='productos',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='costo_almacenamiento',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='valor_inventario',
        ),
        migrations.AddField(
            model_name='cliente',
            name='empresa',
            field=models.ForeignKey(db_column='rut_empresa', default=1, on_delete=django.db.models.deletion.CASCADE, to='core.empresa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='empresa',
            field=models.ForeignKey(db_column='rut_empresa', default=1, on_delete=django.db.models.deletion.CASCADE, to='core.empresa'),
            preserve_default=False,
        ),
    ]
