from django.db import models


class Universe(models.Model):
    name = models.CharField(max_length=30)
    acceleration = models.DecimalField(default=1, max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name
