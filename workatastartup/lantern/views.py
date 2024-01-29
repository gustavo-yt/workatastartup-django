import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Item
from lantern_django import L2Distance, TextEmbedding

def create_item(request):
    item = Item(title="Full Stack Developer", country="US", company_name="Google", city="San Francisco", state="CA", embedding=[1, 2, 3])
    item.save()

    item = {
        "title": item.title,
        "country": item.country,
        "company_name": item.company_name,
        "city": item.city,
        "state": item.state,
        "embedding": item.embedding
    }

    return JsonResponse({"item": item})


@csrf_exempt
def index(request):
    params = json.loads(request.body)['params']

    description = params[0]
    language = params[1]
    country = params[2]
    embedding = params[3]

    distance = L2Distance('embedding', TextEmbedding(
        embedding, 'python'))
    results = Item.objects.filter(
        country=country
    ).annotate(distance=distance).order_by('distance')[:5]

    results_list = [{
        "title": result.title,
        "country": result.country,
        "company_name": result.company_name,
        "city": result.city,
        "state": result.state,
        "distance": result.distance
    } for result in results]

    return JsonResponse({"results": results_list})
