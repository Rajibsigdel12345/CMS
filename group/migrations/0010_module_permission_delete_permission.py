# Generated by Django 5.1.1 on 2024-09-23 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0009_alter_module_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='permission',
            field=models.JSONField(default={'add': False, 'delete': False, 'update': False, 'view': False}),
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
    ]
