# Generated by Django 5.0.1 on 2024-03-27 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_alter_institution_course_no_of_mock_tests'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprogressdata',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
