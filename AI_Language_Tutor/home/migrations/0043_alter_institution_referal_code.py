# Generated by Django 5.0.1 on 2024-03-20 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_alter_institution_referal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='referal_code',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]
