from django.shortcuts import render
from django.http import JsonResponse
from . import models
from django.forms.models import model_to_dict
from extract import plotly_obj_to_json, plot_entity, preprocess_entities, get_all_possible_charts, get_one_figure_by_entity
# Create your views here.

import pickle

try:
    search_engine = pickle.load(open('search.pkl', 'rb'))
except FileNotFoundError:
    print('No search.pkl file found')
    pass


def search(request):
    query = request.GET['q']
    result = search_engine.search(query)
    index_ids = list(map(lambda x: x[0], result))
    entities = models.Data.objects.filter(index_id__in=index_ids)
    entities = [model_to_dict(r) for r in entities]
    return JsonResponse(entities, safe=False)


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
    charts = []
    for entity in entities:
        charts.append(get_one_figure_by_entity(entity))
        # for chart in get_all_possible_charts(entity):
        #     charts.append(plotly_obj_to_json(chart))
    # response = [plotly_obj_to_json(plot_entity(entity)) for entity in entities]
    response = charts
    return JsonResponse(response, safe=False)
