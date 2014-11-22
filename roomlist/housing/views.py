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
