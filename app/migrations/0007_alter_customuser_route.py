# Generated by Django 4.1.7 on 2023-05-20 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_destination_route_path_remove_route_fees_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='route',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.destination'),
        ),
    ]
