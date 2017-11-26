from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
import pytz

# from apps.locations.models import Planet
# from apps.economy.models import Resource


LOCATIONS = (
    (0, 'planetary surface'),
    (1, 'moon surface')
)


# class Building(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     image = models.ImageField(upload_to='buildings', null=True, blank=True)
#     base_cost_metal = models.PositiveIntegerField(default=0)
#     base_cost_crystal = models.PositiveIntegerField(default=0)
#     base_cost_deuter = models.PositiveIntegerField(default=0)
#     base_energy_use = models.PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return self.name


