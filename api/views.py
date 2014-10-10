from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the RoomList index.")

def room(request, room_number):
    return HttpResponse("You are looking up room number %s." % room_number)
