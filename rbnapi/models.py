# coding: utf-8
from django.conf import settings
from django.db import models


class ScientificName(models.Model):
    scientific_name = models.TextField(verbose_name=u"Scientific Name", unique=True)

    def __str__(self):
        return f"{self.scientific_name}".title()

    class Meta:
        ordering = ["-scientific_name"]


class BirdNameDatabase(models.Model):
    scientific_name = models.ForeignKey(ScientificName, related_name='bird_name', on_delete=models.CASCADE)
    bird_name = models.TextField(verbose_name=u"Bird Name", unique=True)

    def __str__(self):
        return f"{self.bird_name}".title()

    class Meta:
        ordering = ["-bird_name"]
        unique_together = ("bird_name", "scientific_name")


class GeneralStatistics(models.Model):
    bird_name = models.ForeignKey("BirdNameDatabase", related_name='statistic', on_delete=models.CASCADE)
    request_count = models.BigIntegerField(verbose_name="Count Number", default=0)
    updated = models.DateTimeField(verbose_name=u"Last Update", auto_now=True)

    def __str__(self):
        return f"{self.bird_name}".title()

    class Meta:
        ordering = ['-updated', ]


class RequestRecord(models.Model):
    statistic = models.ForeignKey("GeneralStatistics", related_name='request_record', on_delete=models.CASCADE)
    client_ip = models.GenericIPAddressField(verbose_name=u"Client IP")
    created = models.DateTimeField(verbose_name=u"Request Date", auto_now_add=True)

    def __str__(self):
        return f"{self.client_ip}"

    class Meta:
        ordering = ['-created', ]

