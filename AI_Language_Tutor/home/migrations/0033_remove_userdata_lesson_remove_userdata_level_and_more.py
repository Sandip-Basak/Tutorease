# Generated by Django 5.0.1 on 2024-02-13 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_arrange_from_lang_arrange_to_lang_match_from_lang_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='level',
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='stage',
        ),
    ]
