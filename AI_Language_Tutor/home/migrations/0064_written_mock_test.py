# Generated by Django 5.0.1 on 2024-04-10 15:06

import home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0063_delete_speech'),
    ]

    operations = [
        migrations.CreateModel(
            name='Written_Mock_Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('institute_code', models.CharField(max_length=15)),
                ('Mock_Test_Number', models.DecimalField(decimal_places=0, default=-1, max_digits=10)),
                ('Total_Marks', models.DecimalField(decimal_places=0, max_digits=4)),
                ('Total_Time', models.DecimalField(decimal_places=0, max_digits=4)),
                ('approved', models.BooleanField(default=False)),
                ('number_of_attempts', models.DecimalField(decimal_places=0, default=1, max_digits=4)),
                ('question_paper', models.FileField(upload_to=home.models.pdf_unique_file_path)),
            ],
        ),
    ]
