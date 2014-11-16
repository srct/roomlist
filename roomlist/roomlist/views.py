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
    template = loader.get_template('buildings.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
