from django.db import models


class EarthQuakeFeed(models.Model):
    title = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=4, decimal_places=2)
    longitude = models.DecimalField(max_digits=4, decimal_places=2)
    magnitude = models.DecimalField(max_digits=2, decimal_places=1)
    time = models.DateTimeField()

    def __str__(self):
        return f'ID = {self.id}, TITLE = {self.title}'
