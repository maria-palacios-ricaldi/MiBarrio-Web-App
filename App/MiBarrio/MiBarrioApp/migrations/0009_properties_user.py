# Generated by Django 4.2.5 on 2023-09-27 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MiBarrioApp', '0008_alter_properties_num_of_bathrooms_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
