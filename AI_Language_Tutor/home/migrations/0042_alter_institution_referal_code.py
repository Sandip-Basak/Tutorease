# Generated by Django 5.0.1 on 2024-03-20 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='referal_code',
            field=models.CharField(max_length=6),
        ),
    ]
