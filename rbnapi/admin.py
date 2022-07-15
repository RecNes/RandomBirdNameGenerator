# -*- codign: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import register

from rbnapi.models import ScientificName, BirdNameDatabase, GeneralStatistics


@register(BirdNameDatabase)
class BirdNameDatabaseAdmin(admin.ModelAdmin):
    list_display = ['bird_name', 'scientific_name']
    ordering = ['bird_name']
    search_fields = ['bird_name']


@register(ScientificName)
class ScientificNameAdmin(admin.ModelAdmin):
    list_display = ['scientific_name']
    ordering = ['scientific_name']
    search_fields = ['scientific_name']


@register(GeneralStatistics)
class GeneralStatisticsAdmin(admin.ModelAdmin):
    list_display = ['bird_name', 'request_count', 'updated']
    ordering = ['updated']
