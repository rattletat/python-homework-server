# Generated by Django 3.0.5 on 2020-05-13 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_auto_20200512_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='relevant',
            field=models.BooleanField(default=True, verbose_name='Gibt an ob die Aufgabe in die Wertung einfließt.'),
        ),
    ]
