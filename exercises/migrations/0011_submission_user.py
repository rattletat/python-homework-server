# Generated by Django 3.0.5 on 2020-04-25 17:59

from django.db import migrations, models
import django.db.models.deletion
import exercises.models


class Migration(migrations.Migration):

    dependencies = [
        ("exercises", "0010_exercise_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uploaded", models.DateTimeField(auto_now_add=True)),
                (
                    "file",
                    models.FileField(upload_to=exercises.models._user_directory_path),
                ),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="exercises.Exercise",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="exercises.User"
                    ),
                ),
            ],
        ),
    ]