from django.shortcuts import render
from django.utils import timezone
from .models import PlayerBuilding, Resource


def index(request):
    first_building = PlayerBuilding.objects.filter(planet=1)[0]
    metal = Resource.objects.get(planet=1, resource_type=1)
    crystal = Resource.objects.get(planet=1, resource_type=2)
    deuterium = Resource.objects.get(planet=1, resource_type=3)

    upgrade_ends_at = first_building.upgrade_ends_at().timestamp()
    one_percent = first_building.upgrade_time() / 100

    context = {
        'building': first_building,
        'upgrade_ends_at': upgrade_ends_at,
        'upgraded_percent': round((first_building.upgrade_ends_at() - timezone.now()).total_seconds() / one_percent),
        'metal': metal,
        'crystal': crystal,
        'deuterium': deuterium
    }

    print(one_percent)
    print(upgrade_ends_at)
    print(first_building.upgrade_time())

    return render(request, 'first_draft/index.html', context)
