# Generated by Django 3.0.5 on 2020-05-29 10:53

import django.core.validators
from django.db import migrations, models
import exercises.helper


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0020_auto_20200522_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='max_upload_size',
            field=models.PositiveIntegerField(default=5000, verbose_name='Maximale Upload Größe in Bytes'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='timeout',
            field=models.PositiveSmallIntegerField(default=10, validators=[django.core.validators.MaxValueValidator(30)], verbose_name='Maximale Testlaufzeit in Sekunden'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='file',
            field=models.FileField(upload_to=exercises.helper.get_submission_path),
        ),
    ]
