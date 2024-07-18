# Generated by Django 5.0.1 on 2024-02-09 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_userprogressdata_stage_alter_userprogressdata_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrange',
            name='code',
            field=models.CharField(default='HIN_ENG', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='code',
            field=models.CharField(default='HIN_ENG', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mcq',
            name='code',
            field=models.CharField(default='HIN_ENG', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mcq_data',
            name='code',
            field=models.CharField(default='HIN_ENG', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mcq_pic_data',
            name='code',
            field=models.CharField(default='HIN_ENG', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='speech',
            name='code',
            field=models.CharField(default='HIN_ENG', max_length=15),
            preserve_default=False,
        ),
    ]
