# coding: utf-8
from rest_framework import serializers
from .models import BirdNameDatabase, ScientificName, GeneralStatistics


class ScientificNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScientificName
        fields = ['scientific_name', ]


class BirdNameSerializer(serializers.ModelSerializer):

    _scientific_name = ScientificNameSerializer(read_only=True, many=True)

    class Meta:
        model = BirdNameDatabase
        depth = 1
        fields = ['bird_name', '_scientific_name']


class GeneralStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralStatistics
        fields = ['bird_name', 'client_ip']
