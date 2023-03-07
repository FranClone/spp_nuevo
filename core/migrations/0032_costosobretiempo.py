# Generated by Django 4.1.6 on 2023-03-03 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_tiempocambio'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostoSobreTiempo',
            fields=[
                ('id_costo_he', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.FloatField(blank=True, null=True)),
                ('rut_empresa', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=20, null=True)),
                ('usuario_crea', models.CharField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=20, null=True)),
                ('fecha_crea', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'COSTO_SOBRE_TIEMPO',
            },
        ),
    ]