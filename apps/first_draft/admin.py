from django.contrib import admin
from django.utils.html import mark_safe
from .models import Building, Moon, Resource, PlayerBuilding, PlayerResource, PlayerPlanet, Universe, PlayerProfile


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type']


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'get_image',
                    'base_cost_metal', 'base_cost_crystal', 'base_cost_deuter', 'base_energy_use']
    list_display_links = ['name']

    def get_image(self, instance):
        image = instance.image
        return mark_safe('<img src="%s">' % image.url) if image else '-'


@admin.register(PlayerBuilding)
class PlayerBuilding(admin.ModelAdmin):
    list_display = ['pk', 'player', 'players_planet', 'building_location', 'building', 'level',
                    'upgrade_ends_at', 'is_upgrading', 'created_at', 'updated_at']
    list_display_links = ['player']


@admin.register(PlayerResource)
class PlayerResourceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'resource', 'amount', 'capacity', 'capacity_exeeded', 'acceleration']
    list_display_links = ['resource']


@admin.register(Moon)
class MoonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'planet', 'player', 'size', 'created_at', 'updated_at']
    list_display_links = ['planet']


@admin.register(PlayerPlanet)
class PlayerPlanet(admin.ModelAdmin):
    list_display = ['pk', 'planet_name', 'player', 'image', 'position', 'sector', 'min_temperature', 'max_temperature',
                    'surface', 'moon_id']
    list_display_links = ['planet_name']


@admin.register(Universe)
class UniverseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'speed']


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'universe']
