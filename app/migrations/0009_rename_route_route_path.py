# Generated by Django 4.1.7 on 2023-05-21 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_destination_end_remove_destination_fees_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='route',
            old_name='route',
            new_name='path',
        ),
    ]
