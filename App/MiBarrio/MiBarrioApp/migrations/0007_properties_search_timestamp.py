# Generated by Django 4.2.5 on 2023-09-27 06:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MiBarrioApp', '0006_remove_properties_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='search_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
