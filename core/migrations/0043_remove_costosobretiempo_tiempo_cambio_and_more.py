# Generated by Django 4.1.7 on 2023-05-02 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_patroncorte_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='costosobretiempo',
            name='tiempo_cambio',
        ),
        migrations.AddField(
            model_name='tiempocambio',
            name='costosobretiempo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.costosobretiempo', verbose_name='Tiempo de Cambio'),
        ),
    ]
