# Generated by Django 5.0.1 on 2024-02-28 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_remove_questiondata_total_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('query', models.TextField()),
                ('response', models.TextField()),
            ],
        ),
    ]
