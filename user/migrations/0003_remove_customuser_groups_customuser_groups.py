# Generated by Django 5.1.1 on 2024-09-20 07:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0005_remove_customgroup_users'),
        ('user', '0002_delete_customgroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='groups',
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='group.customgroup'),
        ),
    ]
