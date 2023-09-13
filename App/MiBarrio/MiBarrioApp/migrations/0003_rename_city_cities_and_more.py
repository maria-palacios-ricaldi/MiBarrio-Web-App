# Generated by Django 4.2.4 on 2023-09-06 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MiBarrioApp', '0002_rename_community_services_searchprofile_community_services_tags_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='City',
            new_name='Cities',
        ),
        migrations.RenameModel(
            old_name='SearchProfile',
            new_name='SearchProfiles',
        ),
        migrations.AlterUniqueTogether(
            name='searchprofiles',
            unique_together={('user', 'sp_name')},
        ),
    ]