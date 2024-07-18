# Generated by Django 5.0.1 on 2024-02-17 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_questiondata'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiondata',
            name='total_questions',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
