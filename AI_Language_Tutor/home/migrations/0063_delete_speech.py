# Generated by Django 5.0.1 on 2024-04-10 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0062_remove_arrange_from_lang_remove_arrange_to_lang_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Speech',
        ),
    ]