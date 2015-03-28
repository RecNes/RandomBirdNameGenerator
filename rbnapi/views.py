# -*- coding: utf-8 -*-
from random import randint
from django.core.context_processors import request
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from rbnapi.models import BirdNameDatabase


def generate_bird_name():
    count = BirdNameDatabase.objects.count() - 1
    index = randint(0, count)
    bn = BirdNameDatabase.objects.all()[index]
    return bn.bird_name.title()


def bird_name_requested(request):
    if request.method == 'GET':
        return HttpResponse(generate_bird_name())


class API():
    def __init__(self):
        pass

    @property
    def get_random_bird_name(self):
        return generate_bird_name()

    def serialize_data(self):
        pass


def start_page(request, title="Random Bird Name Generator"):
    """
        Site ana sayfası.
    """
    content = {'title': title}
    return render_to_response('index.html', content, context_instance=RequestContext(request, {}))