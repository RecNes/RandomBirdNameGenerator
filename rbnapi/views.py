# -*- coding: utf-8 -*-
from random import randint
from django import forms
from django.core import serializers
from django.core.context_processors import request
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_protect
from rbnapi.models import BirdNameDatabase
from rbnapi.rb_logger import log


def generate_bird_name():
    count = BirdNameDatabase.objects.count() - 1
    index = randint(0, count)
    bn = BirdNameDatabase.objects.all()[index]
    log.info("{} / {}".format(bn.bird_name, bn.scientific_name.scientific_name))
    return bn.bird_name, bn.scientific_name.scientific_name


class RBNForm(forms.Form):
    sci_check = forms.BooleanField(required=False, label="Scientific Name", initial=False)


@csrf_protect
def bird_name_requested(request):
    if request.method == 'POST':
        form = RBNForm(request.POST)
        if form.is_valid():
            sci_check = form.cleaned_data['sci_check']
            bn = generate_bird_name()
            if sci_check:
                return HttpResponse("{},{}".format(bn[0].title(), bn[1].title()))
            else:
                return HttpResponse(generate_bird_name()[0].title())


def start_page(request, title="Random Bird Name Generator"):
    """
        Site ana sayfası.
    """
    content = {'title': title}
    return render_to_response('index.html', content, context_instance=RequestContext(request, {}))