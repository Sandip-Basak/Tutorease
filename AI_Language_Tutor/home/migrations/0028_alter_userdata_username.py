# Generated by Django 5.0.1 on 2024-02-13 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_remove_userdata_total_lessons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='username',
            field=models.CharField(max_length=150, primary_key=True, serialize=False),
        ),
    ]
