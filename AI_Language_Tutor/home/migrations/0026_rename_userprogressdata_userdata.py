# Generated by Django 5.0.1 on 2024-02-13 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_remove_userprogressdata_id_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProgressData',
            new_name='UserData',
        ),
    ]