# coding: utf-8
from django.db import models


class ScientificName(models.Model):
    scientific_name = models.TextField(verbose_name=u"Scientific Name", unique=True)

    def __unicode__(self):
        return self.scientific_name


class BirdNameDatabase(models.Model):
    scientific_name = models.ForeignKey(ScientificName, on_delete=models.CASCADE)
    bird_name = models.TextField(verbose_name=u"Bird Name", unique=True)

    def __unicode__(self):
        return self.bird_name

    class Meta:
        unique_together = ("bird_name", "scientific_name")


class GeneralStatistics(models.Model):
    bird_name = models.ForeignKey(BirdNameDatabase, on_delete=models.CASCADE)
    client_ip = models.GenericIPAddressField(verbose_name=u"Client IP")
    created = models.DateTimeField(verbose_name=u"Request Date", auto_now_add=True)

    def __unicode__(self):
        return self.created

    class Meta:
        ordering = ['created', ]
