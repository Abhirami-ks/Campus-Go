# Generated by Django 4.1.7 on 2023-05-21 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_route_route_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='end',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='start',
            field=models.CharField(max_length=100, null=True),
        ),
    ]