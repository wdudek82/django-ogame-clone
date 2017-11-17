from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    acceleration = models.DecimalField(default=1, max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class PlayerProfile(models.Model):
    user = models.OneToOneField(User)
    universe = models.ForeignKey(Universe)

    def __str__(self):
        return str(self.user)


class Moon(models.Model):
    planet = models.OneToOneField('Planet')
    size = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}:{}'.format(self.pk, self.planet)

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
    # TODO: Calculate this inside a method field
    free_sufrace = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.planet_name

    def moon_id(self):
        return self.moon if self.moon else '-'


# TODO: On save, should send pre_save signal to resources to save current state
# TODO: withoud that after changing level (L) of a mine/refinery "accumulated" will be
# TODO: instantly calculated incorrectly
class PlayerBuilding(models.Model):
    LOCATIONS = (
        (0, 'planetary surface'),
        (1, 'moon surface')
    )

    building = models.ForeignKey(Building)
    planet = models.ForeignKey(Planet)
    building_location = models.IntegerField(choices=LOCATIONS, default=1)
    level = models.PositiveIntegerField(default=0)
    upgrade_ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['planet', 'building_location', 'building']

    def __str__(self):
        return '{}:{}:{}'.format(self.pk, self.building_location, self.building)

    def is_upgrading(self):
        """
        Check if building is upgrading by checking if upgrade_end date was set,
        and is a future date. In other case set update_date to null, and
        return boolean
        """
        now = timezone.now()
        upgrade_ends_at = self.upgrade_ends_at
        if upgrade_ends_at and upgrade_ends_at <= now:
            upgrade_ends_at = None
            self.save()
        return bool(upgrade_ends_at)


# TODO: on save() - save amount = accumulated
class Resource(models.Model):
    PERCENT = (
        ((num, num) for num in range(0, 101))
    )

    RESOURCE_TYPE = (
        (1, 'metal'),
        (2, 'crystal'),
        (3, 'deuter')
    )

    resource_type = models.IntegerField(choices=RESOURCE_TYPE)
    location = models.ForeignKey(Planet)
    amount = models.PositiveIntegerField(default=0)
    capacity = models.IntegerField(default=10000)
    production_speed = models.PositiveIntegerField(choices=PERCENT, default=100)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['resource_type', 'location']

    def __str__(self):
        return ''.format(self.pk, self.resource_type, self.location)

    def capacity_exeeded(self):
        """
        If planet's capacity was exeeded, stop production
        of a given resource and set 'overflow' to True
        :return: boolean
        """
        overflow = self.accumulated() > self.capacity
        if overflow:
            self.production_speed = 0
            self.save()
        return overflow

    def produced_per_hour(self):
        """
        production = acceleration * 30 * level * 1.1**level
        """
        # TODO: Need to adjust it for crystal, and - especially - deuter

        universe_acceleration = float(self.location.owner.universe.acceleration)
        resource = self.resource_type
        generator_lvl = PlayerBuilding.objects.get(
            planet=self.location, building=resource
        ).level

        base_production = universe_acceleration * 30 * generator_lvl * 1.1**generator_lvl
        return base_production * (self.production_speed / 100)

    def accumulated(self):
        # Update resource's amount
        now = timezone.now()
        td = (now - self.modified).total_seconds()

        return self.amount + round(self.produced_per_hour() / 3600 * td)
