from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.profiles.models import PlayerProfile


class Moon(models.Model):
    planet = models.OneToOneField('Planet')
    size = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.pk)

    def player(self):
        return self.planet.owner.user


class Planet(models.Model):
    POSITION = (
        ((num+1, num) for num in range(1, 9))
    )

    planet_name = models.CharField(max_length=30)
    owner = models.ForeignKey(PlayerProfile)
    image = models.ImageField(null=True, blank=True)
    position = models.PositiveIntegerField(choices=POSITION, default=5)
    # TODO: Create function, that calculates sector for the home planet
    sector = models.PositiveIntegerField()
    # TODO: Create function calculating base production modifies base on min-max temps
    min_temperature = models.IntegerField(default=0)
    max_temperature = models.IntegerField(default=0)
    surface = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.planet_name

    def free_surface(self):
        building_count = self.buildings.count()
        return self.surface - building_count

    def moon_id(self):
        return self.moon if self.moon else '-'


@receiver(signal=post_save, sender=Planet)
def create_generator_and_recources(*args, **kwargs):

    # create:
    # metal mine lvl 0 + metal (resource)
    # crystal mine lvl 0+ ...
    # deuterium synthesizer lvl 0 + ...
    pass
