# Python
import os.path
import json
import datetime
# Django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# DRF
# from rest_framework.parsers import JSONParser

# Create your views here.
from .models import NYSEMin, NYSEDay, NASDAQMin, NASDAQDay, IndexesDay, IndexesMin, Fundamental


@csrf_exempt
def symbol_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        symbols = NASDAQDay.objects.filter(
            # symbol='AAPL',
            symbol__in=['AAPL'],
            datetime__gte=datetime.date(2019, 10, 1),
            datetime__lt=datetime.date(2020, 4, 1)
        ).order_by('symbol', 'datetime_epoch'
                   ).distinct('symbol', 'open', 'high', 'low', 'close', 'volume', 'datetime_epoch', 'datetime'
                              )

        _dict = {
            'symbol': [row.symbol for row in symbols],
            'open': [row.open for row in symbols],
            'high': [row.high for row in symbols],
            'low': [row.low for row in symbols],
            'close': [row.close for row in symbols],
            'volume': [row.volume for row in symbols],
            'datetime_epoch': [row.datetime_epoch for row in symbols],
            'datetime': [row.datetime.isoformat() for row in symbols],
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type='application/javascript; charset=utf8'
        )

    return HttpResponse('Hello World')


@csrf_exempt
def symbol_detail(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        symbol = request.GET['symbol'].upper()
        start_date = request.GET['start_date'].split('-')
        start_date = [int(row) for row in start_date]

        end_date = request.GET['end_date'].split('-')
        end_date = [int(row) for row in end_date]
        print(symbol)
        symbols = NASDAQDay.objects.filter(
            symbol=symbol,
            datetime__gte=datetime.date(
                start_date[0], start_date[1], start_date[2]),
            datetime__lte=datetime.date(end_date[0], end_date[1], end_date[2])
        ).order_by('symbol', 'datetime_epoch'
                   ).distinct('symbol', 'open', 'high', 'low', 'close', 'volume', 'datetime_epoch', 'datetime'
                              )

        _dict = {
            'symbol': [row.symbol for row in symbols],
            'open': [row.open for row in symbols],
            'high': [row.high for row in symbols],
            'low': [row.low for row in symbols],
            'close': [row.close for row in symbols],
            'volume': [row.volume for row in symbols],
            'datetime_epoch': [row.datetime_epoch for row in symbols],
            'datetime': [row.datetime.isoformat() for row in symbols],
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type='application/javascript; charset=utf8'
        )

    return HttpResponse('Hello World')


@csrf_exempt
def example(request):
    """
    Returns an example of what the frontend expects to generate the visualizations.
    """
    if request.method == 'GET':
        fp = os.path.abspath(os.path.dirname(
            os.path.abspath(__file__))) + "/analysis/output_18Apr.json"
        with open(fp, 'r') as f:
            data = json.load(f)

            return HttpResponse(
                json.dumps(data),
                content_type='application/javascript; charset=utf8'
            )

    return JsonResponse(serializer.errors, status=400)
