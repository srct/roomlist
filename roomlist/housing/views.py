from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from housing.models import Building, Room, Student

from braces.views import LoginRequiredMixin

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

# update a student

# update a room

# update a building
