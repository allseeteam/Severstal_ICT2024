from django.shortcuts import render
from django.http import JsonResponse
from . import models
from django.forms.models import model_to_dict
# Create your views here.

import pickle

search_engine = pickle.load(open('search.pkl', 'rb'))


def search(request):
    query = request.GET['q']
    result = search_engine.search(query)
    return JsonResponse(result, safe=False)


def make_report(request):
    report_ids = request.GET['ids']
    if report_ids:
        report_ids = report_ids.split(',')
    else:
        return JsonResponse({})
    res = models.Data.objects.all()
    res = [model_to_dict(r) for r in res]
    return JsonResponse(res, safe=False)
