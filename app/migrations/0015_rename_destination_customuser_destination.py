# Generated by Django 4.1.7 on 2023-05-22 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_customuser_destination'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='Destination',
            new_name='destination',
        ),
    ]