# Generated by Django 5.1.1 on 2024-09-20 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_remove_permission_module_module_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customgroup',
            name='permissions',
        ),
        migrations.AddField(
            model_name='customgroup',
            name='module',
            field=models.ManyToManyField(to='group.module'),
        ),
    ]
