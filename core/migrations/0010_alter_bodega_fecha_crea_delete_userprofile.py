# Generated by Django 4.1.7 on 2023-03-24 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_userprofile_empresa_alter_userprofile_rut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodega',
            name='fecha_crea',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
