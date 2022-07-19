# -*- codign: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import register

from rbnapi.models import RequestRecord, ScientificName, BirdNameDatabase, GeneralStatistics


@register(BirdNameDatabase)
class BirdNameDatabaseAdmin(admin.ModelAdmin):
    list_display = ['formatted_bird_name', 'scientific_name']
    ordering = ['bird_name']
    search_fields = ['bird_name']

    def formatted_bird_name(self, obj):
        return obj.bird_name.title()

    formatted_bird_name.admin_order_field = 'bird_name'
    formatted_bird_name.short_description = 'Bird Name'


@register(ScientificName)
class ScientificNameAdmin(admin.ModelAdmin):
    list_display = ['formatted_scientific_name']
    ordering = ['scientific_name']
    search_fields = ['scientific_name']

    def formatted_scientific_name(self, obj):
        return obj.scientific_name.title()

    formatted_scientific_name.admin_order_field = 'scientific_name'
    formatted_scientific_name.short_description = 'Scientific Name'


@register(GeneralStatistics)
class GeneralStatisticsAdmin(admin.ModelAdmin):
    list_display = ['bird_name', 'request_count', 'formatted_updated']
    ordering = ['-updated']

    def formatted_updated(self, obj):
        return obj.updated.strftime(settings.DATETIME_FORMAT)

    formatted_updated.admin_order_field = 'created'
    formatted_updated.short_description = 'Last Update'


@register(RequestRecord)
class RequestRecordAdmin(admin.ModelAdmin):
    list_display = ['client_ip', 'statistic', 'formatted_created']
    ordering = ['-created']

    def formatted_created(self, obj):
        return obj.created.strftime(settings.DATETIME_FORMAT)

    formatted_created.admin_order_field = 'created'
    formatted_created.short_description = 'Request Date'
