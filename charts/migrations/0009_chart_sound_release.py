# Generated by Django 4.2.3 on 2023-07-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "charts",
            "0008_chart_comp_artist_chart_sound_likes_chart_sound_play_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="chart",
            name="sound_release",
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]