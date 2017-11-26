from django.contrib import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'resource_type', 'planet', 'location', 'modified', 'amount', 'accumulated',
                    'produced_per_hour',
                    'capacity', 'reached_max_capacity', 'production_speed']
    list_display_links = ['resource_type']
    # readonly_fields = ['amount']
