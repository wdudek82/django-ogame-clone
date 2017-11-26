from django.contrib import admin
from django.utils.html import mark_safe
from .models import Moon, Planet


@admin.register(Moon)
class MoonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'planet', 'size', 'created_at', 'updated_at']
    list_display_links = ['planet']


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ['pk', 'planet_name', 'owner', 'get_image', 'position', 'sector',
                    'min_temperature', 'max_temperature', 'surface', 'free_surface', 'moon_id']
    list_display_links = ['planet_name']

    def get_image(self, instance):
        image = instance.image
        return mark_safe('<img src="%s">' % image.url) if image else '-'
    get_image.short_description = 'image'
