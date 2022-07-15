# coding: utf-8
import logging
from datetime import timedelta
from random import randint

import rest_framework.status
from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from rbnapi.models import BirdNameDatabase, GeneralStatistics, RequestRecord
from .serializers import BirdNameSerializer

log = logging.getLogger(__name__)


class GetBirdName(APIView):
    """
    Birdname REST APIView
    """

    @staticmethod
    def extract_ip_from(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0]
        else:
            client_ip = request.META.get('REMOTE_ADDR')

        return client_ip

    @staticmethod
    def check_request_limit(client_ip):
        end_date = timezone.now()
        start_date = end_date - timedelta(minutes=1)
        request_count = RequestRecord.objects.filter(
            client_ip=client_ip, created__gte=start_date, created__lte=end_date
        ).count()
        return request_count >= 10

    @staticmethod
    def save_general_statistics(client_ip, bn):
        gs, created = GeneralStatistics.objects.get_or_create(bird_name=bn)
        gs.request_count += 1
        gs.save()
        RequestRecord(statistic=gs, client_ip=client_ip).save()
        return GeneralStatistics.objects.count()

    def get(self, request):
        client_ip = self.extract_ip_from(request)
        is_limited = self.check_request_limit(client_ip)
        if is_limited:
            return Response({}, status=rest_framework.status.HTTP_403_FORBIDDEN)
        count = BirdNameDatabase.objects.count() - 1
        index = randint(0, count)
        bn = BirdNameDatabase.objects.all()[index]
        serialized = BirdNameSerializer(bn, many=False)
        self.save_general_statistics(client_ip, bn)
        log.info("{} / {}".format(bn.bird_name, bn.scientific_name.scientific_name))
        return Response(serialized.data)


def start_page(request, title="Random Bird Name Generator"):
    """Home page view"""
    content = {'title': title, 'count': GeneralStatistics.objects.count()}
    return render(request, 'index.html', content)
