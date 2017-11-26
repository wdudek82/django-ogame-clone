from django.db import models
from django.contrib.auth.models import User
from apps.universes.models import Universe


class PlayerProfile(models.Model):
    user = models.OneToOneField(User)
    universe = models.ForeignKey(Universe)

    def __str__(self):
        return str(self.user)
