from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader

from api.models import Building, Room

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def buildings(request):
    building_list = Building.objects.order_by('name')[:5]
    template = loader.get_template('buildings.html')
    context = RequestContext(request, {
        'building_list' : building_list,
    })
    return HttpResponse(template.render(context))
