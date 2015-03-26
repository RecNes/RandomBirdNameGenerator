# -*- coding: utf-8 -*-
from django.core.context_processors import request
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from rbnapi.models import BirdNameDatabase


class API():
    def __init__(self):
        pass

    @property
    def get_random_bird_name(self):
        return BirdNameDatabase.object.order_by('?')[0]

    def serialize_data(self):
        pass


def start_page(request, title="Random Bird Name Generator"):
    """
        Site ana sayfası.
    """
    content = {'title': title}  # 'debug': settings.DEBUG
    return render_to_response('index.html', content, context_instance=RequestContext(request, {}))