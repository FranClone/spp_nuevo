# Generated by Django 4.2.4 on 2023-10-31 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0118_lineahhdisponible_cantidad_hh'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rendimiento_Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rendimiento', models.IntegerField(blank=True, null=True)),
                ('patron_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.patroncorte')),
                ('producto_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
            ],
            options={
                'db_table': 'Rendimiento_Producto',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='patron_corte',
            field=models.ManyToManyField(through='core.Rendimiento_Producto', to='core.patroncorte'),
        ),
    ]
