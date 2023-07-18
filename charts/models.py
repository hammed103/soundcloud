from django.db import models

class Chart(models.Model):
    title = models.CharField(max_length=100,)
    previous_position = models.IntegerField(null=True)
    current_position = models.IntegerField()
    link = models.URLField()
    indicator = models.IntegerField(null=True)
    spot_name = models.CharField(max_length=100,null=True)
    spot_url = models.URLField(null=True)
    comp_name = models.CharField(max_length=100,null=True)
    comp_url = models.URLField(null=True)

