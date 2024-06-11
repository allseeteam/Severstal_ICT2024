from django.shortcuts import render
from django.http import JsonResponse
from . import models
from django.forms.models import model_to_dict
from extract import plotly_obj_to_json, plot_entity, preprocess_entities
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

    entities = models.Data.objects.filter(id__in=report_ids)
    entities = [model_to_dict(r) for r in entities]
    for entity in entities:
        entity['frame'] = entity['data']
        entity['meta'] = entity['meta_data']['title']

    entities = preprocess_entities(entities)
    response = [plotly_obj_to_json(plot_entity(entity)) for entity in entities]
    return JsonResponse(response, safe=False)
