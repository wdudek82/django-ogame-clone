from django.contrib import admin
from django.utils.html import mark_safe
from django.utils import timezone
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
    list_display = ['pk', 'building', 'planet', 'building_location', 'current_level', 'get_upgrade_time',
                    'upgrade_started_at', 'upgrade_ends_at', 'is_upgrading', 'created_at', 'updated_at']
    list_display_links = ['building']
    readonly_fields = ['current_level']

    def get_upgrade_time(self, instance):
        td = timezone.timedelta(seconds=instance.upgrade_time())
        d = timezone.datetime(1, 1, 1) + td
        upgrade_datetime_string = '{}d {}h {}m {}s'.format(d.day-1, d.hour, d.minute, d.second)
        return upgrade_datetime_string
    get_upgrade_time.short_description = 'time to upgrade'


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
