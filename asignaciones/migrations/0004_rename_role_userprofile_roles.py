# Generated by Django 4.2.4 on 2023-10-04 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asignaciones', '0003_alter_userprofile_role_delete_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='role',
            new_name='roles',
        ),
    ]
