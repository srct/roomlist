# standard library imports
from __future__ import absolute_import, print_function, unicode_literals
# core django imports
from django.views.generic import DetailView, ListView
# third party imports
from braces.views import LoginRequiredMixin
# imports from your apps
from .models import Building, Floor, Room
from accounts.models import Student


# a list of neighborhoods and their buildings
class ListBuildings(LoginRequiredMixin, ListView):
    model = Building
    queryset = Building.objects.all()
    # paginate_by
    context_object_name = 'buildings'
    template_name = 'list_buildings.html'

    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(ListBuildings, self).get_context_data(**kwargs)
        context['rappahannock'] = Building.objects.filter(neighbourhood='ra').order_by('name')
        context['shenandoah'] = Building.objects.filter(neighbourhood='sh').order_by('name')
        context['aquia'] = Building.objects.filter(neighbourhood='aq').order_by('name')
        return context


# building floors, other information
class DetailBuilding(LoginRequiredMixin, DetailView):
    model = Building
    slug_field = 'slug__iexact'
    context_object_name = 'building'
    template_name = 'detail_building.html'

    login_url = 'login'

    def get_object(self):
        url_parts = self.request.get_full_path().split('/')
        # ['', 'housing', 'building',]
        building_name = url_parts[2].replace('-', ' ').title()
        building = Building.objects.get(name=building_name)
        return building

    def get_context_data(self, **kwargs):
        context = super(DetailBuilding, self).get_context_data(**kwargs)
        context['floors'] = Floor.objects.filter(building=self.get_object()).order_by('number')
        return context


# this lists the rooms on the floor
class DetailFloor(LoginRequiredMixin, DetailView):
    model = Floor
    context_object_name = 'floor'
    template_name = 'detail_floor.html'

    def get_object(self):
        url_parts = self.request.get_full_path().split('/')
        # ['', 'housing', 'building', 'floor', ]
        building_name = url_parts[2].replace('-', ' ').title()
        floor_number = url_parts[3]
        building = Building.objects.get(name=building_name)
        floor = Floor.objects.get(number=floor_number,
                                  building=building)
        return floor

    def get_context_data(self, **kwargs):
        context = super(DetailFloor, self).get_context_data(**kwargs)

        requesting_student = Student.objects.get(user=self.request.user)

        context['students'] = Student.objects.visible(requesting_student, self.get_object())
        context['notOnFloor'] = not(requesting_student in self.get_object())
        context['notInBuilding'] = not(requesting_student in self.get_object().building)
        return context


class DetailRoom(LoginRequiredMixin, DetailView):
    model = Room
    context_object_name = 'room'
    template_name = 'detail_room.html'

    def get_object(self):
        url_parts = self.request.get_full_path().split('/')
        # ['', 'housing', 'building', 'floor', 'room', ]
        building_name = url_parts[2].replace('-', ' ').title()
        floor_number = url_parts[3]
        room_number = url_parts[4].upper()
        building = Building.objects.get(name=building_name)
        floor = Floor.objects.get(number=floor_number,
                                  building=building)
        room = Room.objects.get(floor=floor,
                                number=room_number)
        return room

    def get_context_data(self, **kwargs):
        context = super(DetailRoom, self).get_context_data(**kwargs)

        requesting_student = Student.objects.get(user=self.request.user)

        context['students'] = Student.objects.visible(requesting_student, self.get_object())
        context['notOnFloor'] = not(requesting_student in self.get_object().floor)
        context['notInBuilding'] = not(requesting_student in self.get_object().floor.building)

        return context
