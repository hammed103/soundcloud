# Generated by Django 4.2.3 on 2023-07-19 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charts", "0009_chart_sound_release"),
    ]

    operations = [
        migrations.AddField(
            model_name="chart",
            name="tags",
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
