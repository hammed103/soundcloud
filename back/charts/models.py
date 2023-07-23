from django.db import models


class Chart(models.Model):
    tags = models.CharField(max_length=100, null=True)
    title = models.CharField(
        max_length=100,
    )
    previous_position = models.IntegerField(null=True)
    current_position = models.IntegerField(null=True)
    link = models.URLField()
    spot_name = models.CharField(max_length=100, null=True)
    spot_url = models.URLField(null=True)
    comp_name = models.CharField(max_length=100, null=True)
    comp_artist = models.CharField(max_length=100, null=True)
    comp_url = models.URLField(null=True)
    sound_likes = models.IntegerField(null=True)
    sound_play = models.IntegerField(null=True)
    sound_repost = models.IntegerField(null=True)
    sound_release = models.DateTimeField()
    lastweek = models.IntegerField(null=True)
