# coding: utf-8
from rest_framework import serializers
from .models import BirdNameDatabase, ScientificName, GeneralStatistics


class BirdNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirdNameDatabase
        fields = '__all__'


class ScientificNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScientificName
        fields = '__all__'


class GeneralStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralStatistics
        fields = '__all__'
