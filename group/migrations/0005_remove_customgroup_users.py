# Generated by Django 5.1.1 on 2024-09-20 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_remove_customgroup_permissions_customgroup_module'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customgroup',
            name='users',
        ),
    ]
