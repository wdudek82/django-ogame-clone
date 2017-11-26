import pytz
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from apps.locations.models import Planet


class Building(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='buildings', null=True, blank=True)
    base_cost_metal = models.PositiveIntegerField(default=0)
    base_cost_crystal = models.PositiveIntegerField(default=0)
    base_cost_deuter = models.PositiveIntegerField(default=0)
    base_energy_use = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class PlayerBuilding(models.Model):
    LOCATIONS = (
        (0, 'planetary surface'),
        (1, 'moon surface')
    )

    building = models.ForeignKey(Building)
    planet = models.ForeignKey(Planet, related_name='buildings')
    building_location = models.IntegerField(choices=LOCATIONS, default=0)
    current_level = models.PositiveIntegerField(default=0)
    new_level = models.PositiveIntegerField(null=True, blank=True)  # to update resource amount before building level
    upgrade_started_at = models.DateTimeField(null=True, blank=True)
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
        lvl = self.current_level or 1
        metal_cost = self.building.base_cost_metal * 1.5**lvl
        crystal_cost = self.building.base_cost_crystal * 1.5**lvl
        rf = 0  # robotic factory
        nf = 0  # nanite factory

        upgrade_time = (metal_cost * crystal_cost) / (2500 * (1 + rf) * 2**nf * uni_speed)

        print(upgrade_time)

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


# class Defense(models):
#     pass


# class PlayerDefense(models):
#     pass


@receiver(pre_save, sender=PlayerBuilding)
def save_resource_state_on_building_update(sender, instance, *args, **kwargs):
    from apps.economy.models import Resource

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
