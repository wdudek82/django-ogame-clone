from django.shortcuts import render
from django.utils import timezone
from .models import PlayerBuilding, Resource


def index(request):
    first_building = PlayerBuilding.objects.filter(planet=1)[0]
    metal = Resource.objects.get(planet=1, resource_type=1)
    crystal = Resource.objects.get(planet=1, resource_type=2)
    deuter = Resource.objects.get(planet=1, resource_type=3)

    context = {
        'building': first_building,
        'upgrade_ends_at': first_building.upgrade_ends_at.timestamp() * 1000,
        'now': timezone.now(),
        'metal': metal,
        'crystal': crystal,
        'deuter': deuter
    }

    return render(request, 'first_draft/index.html', context)
