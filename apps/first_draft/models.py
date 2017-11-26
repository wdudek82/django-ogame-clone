from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
import pytz


LOCATIONS = (
    (0, 'planetary surface'),
    (1, 'moon surface')
)


class Building(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='buildings', null=True, blank=True)
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
    # TODO: Calculate this inside a method field
    free_sufrace = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.planet_name

    def moon_id(self):
        return self.moon if self.moon else '-'


class PlayerBuilding(models.Model):
    building = models.ForeignKey(Building)
    planet = models.ForeignKey(Planet)
    building_location = models.IntegerField(choices=LOCATIONS, default=0)
    current_level = models.PositiveIntegerField(default=0)
    new_level = models.PositiveIntegerField(null=True, blank=True)  # to update resource amount before building level
    upgrade_started_at = models.DateTimeField(null=True, blank=True)
    # upgrade_ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['planet', 'building_location', 'building']

    def __str__(self):
        return '{}:{}:{}'.format(self.pk, self.building_location, self.building)

    def is_upgrading(self):
        if self.upgrade_started_at and self.upgrade_ends_at():
            return self.upgrade_started_at <= timezone.datetime.now(tz=pytz.UTC) <= self.upgrade_ends_at()

    def upgrade_time(self):
        """
        How long it take to upgrade building to the next level
        """
        uni_speed = float(self.planet.owner.universe.acceleration)
        lvl = self.current_level
        metal_cost = self.building.base_cost_metal * 1.5**lvl
        crystal_cost = self.building.base_cost_crystal * 1.5**lvl
        rf = 0  # robotic factory
        nf = 0  # nanite factory

        upgrade_time = (metal_cost * crystal_cost) / (2500 * (1 + rf) * 2**nf * uni_speed)
        return upgrade_time

    def upgrade_ends_at(self):
        upgrade_time = self.upgrade_time()
        upgrade_started = self.upgrade_started_at
        if upgrade_started:
            upgrade_ends_at = upgrade_started + timezone.timedelta(seconds=upgrade_time)
            if upgrade_ends_at >= timezone.datetime.now(tz=pytz.UTC):
                return upgrade_ends_at
            else:
                self.current_level += 1
                self.upgrade_started_at = None
                self.save()
        return None

class Resource(models.Model):
    PERCENT = (
        ((num, num) for num in range(0, 101))
    )

    RESOURCE_TYPE = (
        (1, 'metal'),
        (2, 'crystal'),
        (3, 'deuterium')
    )

    resource_type = models.IntegerField(choices=RESOURCE_TYPE)
    planet = models.ForeignKey(Planet)
    location = models.IntegerField(choices=LOCATIONS, default=1)
    additional_amount = models.PositiveIntegerField(default=0)
    amount = models.PositiveIntegerField(default=0)
    capacity = models.IntegerField(default=10000)
    production_speed = models.PositiveIntegerField(choices=PERCENT, default=100)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['resource_type', 'planet', 'location']

    def __str__(self):
        return ''.format(self.pk, self.resource_type, self.location)

    def reached_max_capacity(self):
        """
        If planet's capacity was exceeded, stop production
        of a given resource and set 'overflow' to True (after next request)
        """
        overflow = self.amount + self.accumulated() >= self.capacity
        if overflow:
            self.amount += self.accumulated()
            self.production_speed = 0
        return overflow

    def produced_per_hour(self):
        """
        production = uni acceleration * 30 * building level * 1.1** building level
        """
        resource_modifier = (30, 20, 10)
        resource = self.resource_type
        min_temp = self.planet.min_temperature
        max_temp = self.planet.max_temperature
        mean_temp = (min_temp + max_temp) / 2
        uni_acc = float(self.planet.owner.universe.acceleration)
        generator_lvl = PlayerBuilding.objects.get(
            planet=self.planet, building=self.resource_type
        ).current_level


        base_production = (
            uni_acc * resource_modifier[resource-1] * generator_lvl * 1.1**generator_lvl
        )

        # If resource is deuterium, take mean planetary temperature into account
        if self.resource_type == 3:
            base_production *= (-0.002 * mean_temp + 1.28)

        return round(base_production * (self.production_speed / 100), 2)

    def accumulated(self):
        """
        Update resource's amount
        """
        now = timezone.now()
        td = (now - self.modified).total_seconds()
        accumulated = round(self.produced_per_hour() / 3600 * td)

        # If capacity was exceeded, cut from the 'accumulated' the overflow value;
        # the goal is to stop accumulating, but at the same time
        # to allow storing more than total capacity, e.g.:
        # when transporters return with their cargo
        total = self.amount + accumulated
        if total >= self.capacity:
            overflow = total - self.capacity
            accumulated -= overflow

        if accumulated < 0:
            accumulated = 0

        return accumulated


# TODO: Write tests to verify, that updating resource amount finally works!!
@receiver(pre_save, sender=Resource)
def update_amount(sender, instance, *args, **kwargs):
    accumulated = instance.accumulated()
    instance.amount += instance.additional_amount + accumulated
    instance.additional_amount = 0


@receiver(pre_save, sender=PlayerBuilding)
def save_resource_state_on_building_update(sender, instance, *args, **kwargs):
    building_id = instance.building.id
    current_level = instance.current_level
    new_level = instance.new_level

    # If building's level was changed, first save the resource it generated
    # to prevent wrong recalculation of "accumulated" value,
    # that uses "produced_per_hour" coefficient dependant on building's level
    if current_level != new_level and new_level:
        if building_id in [1, 2, 3]:
            resource = Resource.objects.get(
                resource_type=building_id,
                planet=instance.planet,
                location=instance.building_location,
            )
            resource.save()
        instance.current_level = new_level
        instance.new_level = None
