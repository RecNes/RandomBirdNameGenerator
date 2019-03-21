# coding: utf-8
from random import randint

from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from rbnapi.models import BirdNameDatabase, GeneralStatistics
from rbnapi.rb_logger import log


def save_general_statistics(request, bn):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    GeneralStatistics(bird_name=bn, client_ip=client_ip).save()
    return GeneralStatistics.objects.count()


def generate_bird_name(request):
    count = BirdNameDatabase.objects.count() - 1
    index = randint(0, count)
    bn = BirdNameDatabase.objects.all()[index]
    count = save_general_statistics(request, bn)
    log.info("{} / {}".format(bn.bird_name, bn.scientific_name.scientific_name))
    return bn.bird_name, bn.scientific_name.scientific_name, count


class RBNForm(forms.Form):
    sci_check = forms.BooleanField(required=False, label="Scientific Name", initial=False)


@csrf_protect
def bird_name_requested(request):
    if request.method == 'POST':
        form = RBNForm(request.POST)
        if form.is_valid():
            sci_check = form.cleaned_data['sci_check']
            bn = generate_bird_name(request)
            print("------------")
            print(bn)
            if sci_check:
                return HttpResponse("{},{},{}".format(bn[0].title(), bn[1].title(), bn[2]))
            else:
                return HttpResponse("{},{}".format(bn[0].title(), bn[2]))


def start_page(request, title="Random Bird Name Generator"):
    """
        Site ana sayfası.
    """
    content = {'title': title, 'count': GeneralStatistics.objects.count()}
    return render(request, 'index.html', content)
