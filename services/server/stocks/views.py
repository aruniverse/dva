# Python
import json, datetime
# Django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# DRF
from rest_framework.parsers import JSONParser

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
			symbol__in= ['AAPL'],
			datetime__gte = datetime.date(2019, 10, 1),
			datetime__lt = datetime.date(2020, 4, 1)
			).order_by('symbol', 'datetime_epoch'
			).distinct('symbol', 'open', 'high', 'close', 'volume', 'datetime_epoch', 'datetime'
			)

		_dict = {
			'symbol'		 : [row.symbol for row in symbols],
			'open'  		 : [row.open for row in symbols],
			'high'  		 : [row.high for row in symbols],
			'close' 		 : [row.close for row in symbols],
			'volume' 		 : [row.volume for row in symbols],
			'datetime_epoch' : [row.datetime_epoch for row in symbols],
			'datetime' 		 : [row.datetime.isoformat() for row in symbols],
		}
		return HttpResponse(
			json.dumps(_dict),
			content_type = 'application/javascript; charset=utf8'
			)

	return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def symbol_detail(request, pk):
	"""
	List all code snippets, or create a new snippet.
	"""
	if request.method == 'GET':
		symbols = NASDAQDay.objects.filter(symbol='AAPL')

		_dict = {
			'symbol'		 : [row.symbol for row in symbols],
			'open'  		 : [row.open for row in symbols],
			'high'  		 : [row.high for row in symbols],
			'close' 		 : [row.close for row in symbols],
			'volume' 		 : [row.volume for row in symbols],
			'datetime_epoch' : [row.datetime_epoch for row in symbols],
			# 'datetime' 		 : [row.datetime for row in symbols],
		}
		print(json.dumps(_dict))
		# print(_dict['open'])
		return HttpResponse(
			json.dumps(_dict),
			content_type = 'application/javascript; charset=utf8'
			)

	return JsonResponse(serializer.errors, status=400)