# Generated by Django 5.0.1 on 2024-03-27 16:51

import home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0054_mock_test_mcq_pic_data_type_2_mock_test_mcq_type_3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mcq_data',
            name='option1_link',
            field=models.FileField(upload_to=home.models.unique_file_path),
        ),
        migrations.AlterField(
            model_name='mcq_data',
            name='option2_link',
            field=models.FileField(upload_to=home.models.unique_file_path),
        ),
        migrations.AlterField(
            model_name='mcq_data',
            name='option3_link',
            field=models.FileField(upload_to=home.models.unique_file_path),
        ),
        migrations.AlterField(
            model_name='mcq_data',
            name='option4_link',
            field=models.FileField(upload_to=home.models.unique_file_path),
        ),
    ]
