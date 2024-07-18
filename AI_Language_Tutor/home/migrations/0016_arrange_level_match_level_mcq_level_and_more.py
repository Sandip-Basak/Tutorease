# Generated by Django 5.0.1 on 2024-01-20 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_mcq_data_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrange',
            name='level',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='level',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mcq',
            name='level',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mcq_pic_data',
            name='level',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='speech',
            name='level',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=1),
            preserve_default=False,
        ),
    ]
