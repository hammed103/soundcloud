# Generated by Django 4.2.3 on 2023-07-17 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("charts", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="chart",
            old_name="song",
            new_name="title",
        ),
        migrations.AddField(
            model_name="chart",
            name="link",
            field=models.URLField(default=None),
            preserve_default=False,
        ),
    ]
