from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    count_request = models.IntegerField()

    def __str__(self) -> str:
        return self.name, self.count_request
