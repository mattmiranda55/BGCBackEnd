from django.db import models


class Graft(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField()
    category = models.CharField()
    regulation = models.CharField()

    def __str__(self):
        return self.name
