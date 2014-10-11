from django.http import HttpResponse

from api.models import Building
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the RoomList index.")

def buildings_list(request):
    building_list = Building.objects.order_by('-name')[:5]
    json = '{"buildings":['
    for p in building_list:
        json += '"'+p.__str__()+'",'
    json = json[:-1]+']}'
    return HttpResponse(json)

def building(request, building):
    return HttpResponse("You are looking up building %s" % building)

def room(request, building, room_number):
    return HttpResponse("You are looking up room number %s in %s" % (room_number, building))
