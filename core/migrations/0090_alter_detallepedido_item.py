# Generated by Django 4.2.5 on 2023-09-28 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0089_empaque_anc_paquete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedido',
            name='item',
            field=models.CharField(max_length=20, null=True),
        ),
    ]