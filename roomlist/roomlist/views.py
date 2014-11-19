from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, logout

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

def login(request):
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AuthenticationForm(data = request.POST)
        # check whether it's valid:
        form.is_valid()
        form_data = form.clean()
        user = form.get_user()
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
        return HttpResponseRedirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AuthenticationForm()
        template = loader.get_template('login.html')
        context = RequestContext(request, {
            'form' : form,
        })
        return HttpResponse(template.render(context))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
