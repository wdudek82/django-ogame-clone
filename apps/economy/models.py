from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from apps.locations.models import Planet


class Resource(models.Model):
    LOCATIONS = (
        (0, 'planetary surface'),
        (1, 'moon surface')
    )

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
    location = models.IntegerField(choices=LOCATIONS, default=0)
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
        from apps.structures.models import PlayerBuilding

        resource_modifier = (30, 20, 10)
        resource = self.resource_type
        min_temp = self.planet.min_temperature
        max_temp = self.planet.max_temperature
        mean_temp = (min_temp + max_temp) / 2
        uni_acc = float(self.planet.owner.universe.acceleration)

        generator_lvl = PlayerBuilding.objects.get(
            planet=self.planet, building=resource
        ).current_level

        base_production = (
            uni_acc * resource_modifier[resource-1] * generator_lvl * 1.1**generator_lvl
        )

        # If resource is deuterium, take mean planetary temperature into account
        if resource == 3:
            base_production *= (-0.002 * mean_temp + 1.28)

        result = round(base_production * (self.production_speed / 100), 2)

        if result == 0 and resource == 1:
            result = 30

        return result

    def accumulated(self):
        """
        Update resource's amount
        """
        now = timezone.now()
        td = (now - self.modified).total_seconds() if self.modified else timezone.now().timestamp()
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


@receiver(pre_save, sender=Resource)
def update_amount(sender, instance, *args, **kwargs):
    accumulated = instance.accumulated()
    instance.amount += instance.additional_amount + accumulated
    instance.additional_amount = 0
