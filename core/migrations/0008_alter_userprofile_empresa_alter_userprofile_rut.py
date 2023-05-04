# Generated by Django 4.1.7 on 2023-03-18 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_abastecimientorollizo_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='empresa',
            field=models.ForeignKey(blank=True, db_column='rut_empresa', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.empresa'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='rut',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]