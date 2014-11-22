from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, logout

from braces.views import LoginRequiredMixin

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from housing.models import Building, Room, Student

# a list of neighborhoods and their buildings
class ListBuildings(LoginRequiredMixin, ListView):
    model = Building
    login_url = '/'

# building floors, other information
class DetailBuilding(LoginRequiredMixin, DetailView):
    model = Building
    login_url = '/'

# this lists the rooms on the floor
class ListRooms(LoginRequiredMixin, ListView):
    model = Room
    login_url = '/'

# this lists students in a room
class DetailRoom(LoginRequiredMixin, ListView):
    model = Room
    login_url = '/'

# details about the student
class DetailStudent(LoginRequiredMixin, DetailStudent):
    model = Student
    login_url = '/'

# update a student

# update a room

# update a building

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
        # check whether it's valid:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
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
