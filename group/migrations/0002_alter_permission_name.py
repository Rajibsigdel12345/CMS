# Generated by Django 5.1.1 on 2024-09-20 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(choices=[('ADD', 'add'), ('VIEW', 'view'), ('UPDATE', 'update'), ('DELETE', 'delete')], max_length=100),
        ),
    ]
