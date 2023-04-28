# Generated by Django 4.1.7 on 2023-04-28 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_calidadproducto_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='linea',
            name='empresa',
            field=models.ForeignKey(db_column='rut_empresa', default='10477088-6', on_delete=django.db.models.deletion.CASCADE, to='core.empresa', verbose_name='Empresa'),
            preserve_default=False,
        ),
    ]
