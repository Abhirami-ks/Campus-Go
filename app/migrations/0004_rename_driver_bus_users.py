# Generated by Django 4.1.7 on 2023-05-19 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_customuser_route'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bus',
            old_name='driver',
            new_name='users',
        ),
    ]
