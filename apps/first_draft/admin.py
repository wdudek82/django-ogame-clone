from django.contrib import admin
from django.utils.html import mark_safe
from .models import Building, Moon, Resource, PlayerBuilding, Planet, Universe, PlayerProfile


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'get_image',
                    'base_cost_metal', 'base_cost_crystal', 'base_cost_deuter', 'base_energy_use']
    list_display_links = ['name']

    def get_image(self, instance):
        image = instance.image
        return mark_safe('<img src="%s">' % image.url) if image else '-'
    get_image.short_description = 'image'


@admin.register(PlayerBuilding)
class PlayerBuilding(admin.ModelAdmin):
    list_display = ['pk', 'building', 'planet', 'building_location', 'current_level',
                    'upgrade_ends_at', 'is_upgrading', 'created_at', 'updated_at']
    list_display_links = ['building']
    readonly_fields = ['current_level']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'resource_type', 'planet', 'location', 'modified', 'amount', 'accumulated',
                    'produced_per_hour',
                    'capacity', 'reached_max_capacity', 'production_speed']
    list_display_links = ['resource_type']
    # readonly_fields = ['amount']


@admin.register(Moon)
class MoonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'planet', 'size', 'created_at', 'updated_at']
    list_display_links = ['planet']


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ['pk', 'planet_name', 'owner', 'get_image', 'position', 'sector',
                    'min_temperature', 'max_temperature', 'surface', 'moon_id']
    list_display_links = ['planet_name']

    def get_image(self, instance):
        image = instance.image
        return mark_safe('<img src="%s">' % image.url) if image else '-'
    get_image.short_description = 'image'


@admin.register(Universe)
class UniverseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'acceleration']
    list_display_links = ['name']


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'universe']
