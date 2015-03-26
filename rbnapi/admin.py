# -*- codign: utf-8 -*-
from django.contrib import admin
from rbnapi.models import ScientificName, BirdNameDatabase


class BirdNameDatabaseAdmin(admin.ModelAdmin):
    list_display = ['bird_name', 'scientific_name']
    ordering = ['bird_name']


class ScientificNameAdmin(admin.ModelAdmin):
    list_display = ['scientific_name']
    ordering = ['scientific_name']


def admin_register(admin_, namespace):
    """
        convenience function to easily register admin classes

        :param admin: result of 'from django.contrib import admin'
        :param namespace: must take a locally called globals

        usage::

            # should be at the end of the admin.py file
            # globals must be called locally as below
        admin_register(admin, namespace=globals())
    """
    for name, model_admin in namespace.copy().iteritems():
        if name.endswith("Admin"):
            model = namespace[name[:-5]]
            try:
                admin_.site.register(model, model_admin)
            except:
                raise


admin_register(admin, namespace=globals())