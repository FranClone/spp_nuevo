# Generated by Django 4.1.6 on 2023-02-06 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nombre',
            field=models.CharField(default='pancho', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='password',
            field=models.CharField(default='pancho', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='rut',
            field=models.CharField(default='pancho', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(max_length=12),
        ),
    ]
