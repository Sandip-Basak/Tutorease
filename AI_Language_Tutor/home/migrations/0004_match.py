# Generated by Django 5.0.1 on 2024-01-11 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_mcq'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_no', models.DecimalField(decimal_places=0, max_digits=2)),
                ('arr1', models.TextField()),
                ('arr2', models.TextField()),
            ],
        ),
    ]
