# Generated by Django 4.1.6 on 2023-02-23 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_linea_alter_bodega_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='rut_empresa',
            field=models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=20),
        ),
    ]
