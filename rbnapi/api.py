# -*- coding: utf-8 -*-
from random import randint
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework import viewsets
from rbnapi.models import BirdNameDatabase


class RBNApiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BirdNameDatabase
        fields = ('url', 'bird_name')


class RBNApiViewSet(viewsets.ModelViewSet):
    count = BirdNameDatabase.objects.count() - 1
    index = randint(0, count)
    queryset = BirdNameDatabase.objects.all()  # [index]
    serializer_class = RBNApiSerializer
