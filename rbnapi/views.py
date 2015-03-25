# -*- coding: utf-8 -*-
from rbnapi.models import BirdNameDatabase


class API():
    def __init__(self):
        pass

    @property
    def get_random_bird_name(self):
        return BirdNameDatabase.object.order_by('?')[0]

    def serialize_data(self):
        pass
