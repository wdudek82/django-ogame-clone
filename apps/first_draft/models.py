from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Resource(models.Model):
    type = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Resources'

    def __str__(self):
        return self.type


class Building(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(null=True, blank=True)
    base_cost_metal = models.PositiveIntegerField(default=0)
    base_cost_crystal = models.PositiveIntegerField(default=0)
    base_cost_deuter = models.PositiveIntegerField(default=0)
    base_energy_use = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Universe(models.Model):
    name = models.CharField(max_length=30)
    speed = models.DecimalField(default=1, max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class PlayerProfile(models.Model):
    user = models.OneToOneField(User)
    universe = models.ForeignKey(Universe)

    def __str__(self):
        return str(self.user)


class Moon(models.Model):
    planet = models.OneToOneField('PlayerPlanet')
    size = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}:{}'.format(self.pk, self.planet)

    def player(self):
        return self.planet.player.user


class PlayerPlanet(models.Model):
    POSITION = (
        ((num+1, num) for num in range(1, 9))
    )

    planet_name = models.CharField(max_length=30)
    player = models.ForeignKey(PlayerProfile)
    image = models.ImageField(null=True, blank=True)
    position = models.PositiveIntegerField(choices=POSITION, default=5)
    # TODO: Create function, that calculates sector for the home planet
    sector = models.PositiveIntegerField()
    # TODO: Create function calculating base production modifies base on min-max temps
    min_temperature = models.IntegerField(default=0)
    max_temperature = models.IntegerField(default=0)
    surface = models.PositiveIntegerField()
    # TODO: Calculate this inside a method field
    free_sufrace = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.planet_name

    def moon_id(self):
        return self.moon if self.moon else '-'


class PlayerBuilding(models.Model):
    LOCATIONS = (
        (0, 'planetary surface'),
        (1, 'moon surface')
    )

    player = models.ForeignKey(PlayerProfile)
    players_planet = models.ForeignKey('PlayerPlanet')
    building_location = models.IntegerField(choices=LOCATIONS, default=0)
    building = models.ForeignKey(Building)
    level = models.PositiveIntegerField(default=0)
    upgrade_ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['player', 'players_planet', 'building_location', 'building']

    def __str__(self):
        return '{}:{}:{}'.format(self.pk, self.player, self.building)

    def is_upgrading(self):
        """
        Check if building is upgrading by checking if upgrade_end date was set,
        and is a future date. In other case set update_date to null, and
        return boolean
        """
        now = timezone.now()
        upgrade_ends_at = self.upgrade_ends_at
        if upgrade_ends_at and upgrade_ends_at <= now:
            upgrade_ends = None
            self.save()
        return bool(upgrade_ends_at)


class PlayerResource(models.Model):
    PERCENT = (
        ((num+1, num) for num in range(0, 101))
    )

    player = models.ForeignKey(PlayerProfile)
    resource = models.ForeignKey(Resource)
    amount = models.PositiveIntegerField(default=0)
    capacity = models.IntegerField(default=10000)
    acceleration = models.PositiveIntegerField(choices=PERCENT, default=100)

    def capacity_exeeded(self):
        """
        If planet's capacity was exeeded, stop production
        of a given resource and set 'overflow' to True
        :return: boolean
        """
        overflow = self.amount > self.capacity
        if overflow:
            self.acceleration = 0
            self.save()
        return overflow
