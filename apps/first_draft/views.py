from django.shortcuts import render, redirect
from django.utils import timezone
from apps.structures.models import PlayerBuilding
from apps.economy.models import Resource


def index(request):
    first_building = PlayerBuilding.objects.filter(planet=1)[0]
    metal = Resource.objects.get(planet=1, resource_type=1)
    crystal = Resource.objects.get(planet=1, resource_type=2)
    deuterium = Resource.objects.get(planet=1, resource_type=3)

    upgrade_starts_at = first_building.upgrade_started_at
    if upgrade_starts_at:
        upgrade_starts_at = upgrade_starts_at.timestamp()

    upgrade_ends_at = first_building.upgrade_ends_at()
    upgraded_percent = 100
    one_percent = first_building.upgrade_time() / 100
    if upgrade_ends_at:
        upgrade_ends_at = upgrade_ends_at.timestamp()
        upgraded_percent = 100 - round((upgrade_ends_at - timezone.now().timestamp()) / one_percent, 1)


    context = {
        'building': first_building,
        'upgrade_started_at': upgrade_starts_at,
        'upgrade_ends_at': upgrade_ends_at,
        'upgraded_percent': upgraded_percent,
        'metal': metal,
        'crystal': crystal,
        'deuterium': deuterium
    }

    return render(request, 'first_draft/index.html', context)


# def cancel_building_upgrade(request):
#     redirect