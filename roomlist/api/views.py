# core django imports
from django.http import HttpResponse
# third party imports
import json
# imports from your apps
from housing.models import Building, Room


def index(request):
    return HttpResponse("Hello, world. You're at the RoomList index.")


def buildings_list(request):
    building_list = Building.objects.order_by('name')[:5]
    jsons = '{"buildings":['
    for p in building_list:
        jsons += '"'+p.__str__()+'":"'+p.address.__str__()+'",'
    jsons = jsons[:-1]+']}'
    return HttpResponse(jsons)


def building(request, buildingName):
    room_list = Room.objects.filter(building__name=''+buildingName).order_by('number')
    jsons = 'Building does not exist'
    if room_list:
        jsons = '{"name":"'+buildingName+'","rooms":['
        for p in room_list:
            jsons += '"'+p.number.__str__()+'":['
            jsons += '"floor":'+p.floor.__str__()+',"bedA":"'+p.bedA.__str__()+'"'
            if p.bedB.__str__() is not '':
                jsons += ',"bedB":"'+p.bedB.__str__()+'"'
            if p.bedC.__str__() is not '':
                jsons += ',"bedC":"'+p.bedC.__str__()+'"'
            if p.bedD.__str__() is not '':
                jsons += ',"bedD":"'+p.bedD.__str__()+'"'
            jsons += '],'
        jsons = jsons[:-1] + ']}'
    return HttpResponse(jsons)


def room(request, building, room_number):
    room_obj = Room.objects.filter(building__name=''+building, number=room_number)

    jsons = "This room does not exist or has not been created"
    if room_obj:
        jsons = '{"building":"'+building+'","number":'+room_number+','
        for p in room_obj:
            jsons += '"floor":'+p.floor.__str__()+',"residents":["bedA":"'+p.bedA.__str__()+'"'
            if p.bedB.__str__() is not '':
                jsons += ',"bedB":"'+p.bedB.__str__()+'"'
            if p.bedC.__str__() is not '':
                jsons += ',"bedC":"'+p.bedC.__str__()+'"'
            if p.bedD.__str__() is not '':
                jsons += ',"bedD":"'+p.bedD.__str__()+'"'
            jsons += ']'
        jsons += ']}'
    return HttpResponse(jsons)


###################JASON trying to JSON in python, so confuzed:
#    if room_obj:
#        jsons = {'building':building, 'number':room_number, 'residents': []}
#        for p in room_obj:
#            jsons.residents[0] =  'bedA':p.bedA.__str__()
#            if p.bedB.__str__() is not '':
#                jsons.residents[1] = 'bedB':p.bedB.__str__()
#            if p.bedC.__str__() is not '':
#                jsons.residents[2] = 'bedC':p.bedC.__str__()
#            if p.bedD.__str__() is not '':
#                jsons.residents[3] = 'bedD':p.bedD.__str__()
#    return HttpResponse(json.dumps(jsons))


def neighbourhood(request, nhood):
    building_list = Building.objects.filter(neighbourhood=''+nhood).order_by('name')
    jsons = 'That neighbourhood has no buildings or does not exist'
    code = 404
    if building_list:
        code = 200
        jsons = '{"neighbourhood":"'+nhood+'","buildings":['
        for p in building_list:
            jsons += '"'+p.__str__()+'",'
        jsons = jsons[:-1]+']}'
    return HttpResponse(jsons, status=code)
