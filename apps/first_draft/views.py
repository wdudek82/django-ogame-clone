from django.shortcuts import render
from .models import PlayerBuilding


def index(request):
    first_building = PlayerBuilding.objects.filter(player_id=1)
    context = {
        'building': first_building[0],
    }
    return render(request, 'first_draft/index.html', context)
