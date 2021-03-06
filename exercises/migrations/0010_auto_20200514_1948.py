# Generated by Django 3.0.5 on 2020-05-14 17:48

import django.core.validators
from django.db import migrations, models
import exercises.helper
import exercises.storage
import exercises.validators


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0009_merge_20200514_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='resources',
            field=models.FileField(default=None, null=True, storage=exercises.storage.OverwriteStorage(), upload_to=exercises.helper.get_resources_path, validators=[exercises.validators.FileValidator(allowed_extensions=['py'], allowed_mimetypes=['text/python', 'text/x-python'])]),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='number',
            field=models.PositiveSmallIntegerField(default=None, editable=False, primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
