from django.http import HttpResponse

from api.models import Building, Room
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

def building(request, buildingName):
    room_list = Room.objects.filter(building__name=""+buildingName)
    json = '{"'+buildingName+'":['
    for p in room_list:
        json += '"'+p.number.__str__()+'":['
        json += '"floor":'+p.floor.__str__()+',"bedA":"'+p.bedA.__str__()+'"'
        if p.bedB.__str__() is not '':
            json += ',"bedB":"'+p.bedB.__str__()+'"'
        if p.bedC.__str__() is not '':
            json += ',"bedC":"'+p.bedC.__str__()+'"'
        if p.bedD.__str__() is not '':
            json += ',"bedD":"'+p.bedD.__str__()+'"'
        json += '],'
    json = json[:-1]+']}'
    return HttpResponse(json)

def room(request, building, room_number):
    return HttpResponse("You are looking up room number %s in %s" % (room_number, building))
