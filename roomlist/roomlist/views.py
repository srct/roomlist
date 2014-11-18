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

def building(request, buildingName):
    building = Building.objects.get(name__iexact=''+buildingName)
    room_list = Room.objects.filter(building__name=''+building.name).order_by('number')
    template = loader.get_template('building.html')
    context = RequestContext(request, {
        'building' : building,
        'room_list' : room_list,
    })
    return HttpResponse(template.render(context))
