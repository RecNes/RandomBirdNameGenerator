# -*- coding: utf-8 -*-

from django.db import models


class ScientificName(models.Model):
    scientific_name = models.TextField(verbose_name=u"Scientific Name", unique=True)

    def __unicode__(self):
        return self.scientific_name


class BirdNameDatabase(models.Model):
    """
    Data will be extracted from:
    https://en.wikipedia.org/wiki/List_of_birds_of_the_world
    """
    scientific_name = models.ForeignKey(ScientificName)
    bird_name = models.TextField(verbose_name=u"Bird Name", unique=True)

    def __unicode__(self):
        return self.bird_name

    class Meta:
        unique_together = ("bird_name", "scientific_name")