# Generated by Django 4.1.7 on 2023-05-02 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_linea_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='rollizolargo',
            name='empresa',
            field=models.ForeignKey(db_column='rut_empresa', default='10477088-6', on_delete=django.db.models.deletion.CASCADE, to='core.empresa', verbose_name='Empresa'),
            preserve_default=False,
        ),
    ]
