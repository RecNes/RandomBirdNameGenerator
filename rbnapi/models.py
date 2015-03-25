# -*- coding: utf-8 -*-

from django.db import models


class BirdNameDatabase(models.Model):
    """
    Data will be extracted from:
    https://en.wikipedia.org/wiki/List_of_birds_of_the_world
    """
    bird_name = models.TextField(verbose_name=u"Bird Name")
    scientific_name = models.TextField(verbose_name=u"Scientific Name")

    def __unicode__(self):
        return self.bird_name

    def _scientific_unicode(self):
        return self.scientific_name
