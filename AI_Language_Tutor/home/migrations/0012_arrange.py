# Generated by Django 5.0.1 on 2024-01-16 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_lessons'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_no', models.DecimalField(decimal_places=0, max_digits=2)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('options', models.TextField()),
                ('number_of_options', models.DecimalField(decimal_places=0, max_digits=2)),
            ],
        ),
    ]
