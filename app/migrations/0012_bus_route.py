# Generated by Django 4.1.7 on 2023-05-22 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_bus_route1_remove_bus_route2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='route',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.route'),
        ),
    ]
