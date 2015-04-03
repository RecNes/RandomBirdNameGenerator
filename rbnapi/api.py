# -*- coding: utf-8 -*-
from random import randint
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework import viewsets
from rbnapi.models import BirdNameDatabase


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class RBNApiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BirdNameDatabase
        fields = ('url', 'bird_name')


class RBNApiViewSet(viewsets.ModelViewSet):
    count = BirdNameDatabase.objects.count() - 1
    index = randint(0, count)
    queryset = BirdNameDatabase.objects.all()  # [index]
    serializer_class = RBNApiSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer