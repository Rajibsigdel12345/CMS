# Generated by Django 5.1.1 on 2024-09-25 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_alter_employee_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
    ]
