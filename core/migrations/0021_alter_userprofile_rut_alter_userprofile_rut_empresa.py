# Generated by Django 4.1.6 on 2023-02-24 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_userprofile_rut_alter_userprofile_rut_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='rut',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]