# Generated by Django 3.0.5 on 2020-04-22 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exercises", "0003_auto_20200422_2128"),
    ]

    operations = [
        migrations.RemoveField(model_name="exercise", name="id",),
        migrations.AlterField(
            model_name="exercise",
            name="number",
            field=models.PositiveSmallIntegerField(
                default=None, primary_key=True, serialize=False
            ),
        ),
    ]
