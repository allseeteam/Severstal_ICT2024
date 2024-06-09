from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

import pickle

search_engine = pickle.load(open('search.pkl', 'rb'))


def search(request):
    query = request.GET['q']
    result = search_engine.search(query)
    return JsonResponse(result, safe=False)
