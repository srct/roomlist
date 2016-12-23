# standard library imports
from __future__ import absolute_import, print_function, unicode_literals
from collections import OrderedDict
# core django imports
from django.views.generic import DetailView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
# third party imports
from braces.views import LoginRequiredMixin
# imports from your apps
from .models import Building, Floor, Room
from accounts.models import Student


# this should be written in cache, to be entirely honest
def shadowbanning(me, other_people):
    # start with only students who are actually blocking anyone
    blockers = [student for student in Student.objects.exclude(blocked_kids=None)]
    # of those students, collect the ones that block *you*
    blocks_me = [student
                 for student in blockers
                 if me in student.blocked_kids.all()]
    if blocks_me:  # python implicit truth evaluation
        student_safety = list(set(other_people) - set(blocks_me))
        return student_safety
    else:
        return other_people


# a list of neighborhoods and their buildings
class ListBuildings(ListView):
    model = Building
    queryset = Building.objects.all()
    # paginate_by
    context_object_name = 'buildings'
    template_name = 'list_buildings.html'

    def get_context_data(self, **kwargs):
        context = super(ListBuildings, self).get_context_data(**kwargs)
        neighbourhoods = (('aq', 'Aquia'),
                          ('ra', 'Rappahannock'),
                          ('sh', 'Shenandoah'))
        # we want our neighbourhoods in alphabetical order
        buildings_by_neighbourhood = OrderedDict()
        # create an ordered dictionary with neighbourhood name, building in said
        # neighbourhood pairings
        for neighbourhood in neighbourhoods:
            # the tuple matrix was necessary because what we'll render for humans
            # is not the string for filtering in the database
            buildings_by_neighbourhood[neighbourhood[1]] = Building.objects.filter(neighbourhood=neighbourhood[0]).order_by('name') 
        # this whole process is done so we don't have template code in triplicate
        # for each neighbourhood
        context['buildings_by_neighbourhood'] = buildings_by_neighbourhood
        return context


# building floors, other information
class DetailBuilding(DetailView):
    model = Building
    slug_field = 'slug__iexact'
    context_object_name = 'building'
    template_name = 'detail_building.html'

    def get_object(self):
        url_parts = self.request.get_full_path().split('/')
        # ['', 'housing', 'building',]
        building_name = url_parts[2].replace('-', ' ').title()
        try:
            building = Building.objects.get(name=building_name)
        except ObjectDoesNotExist:
            raise Http404
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

    login_url = 'login'

    def get_object(self):
        url_parts = self.request.get_full_path().split('/')
        # ['', 'housing', 'building', 'floor', ]
        building_name = url_parts[2].replace('-', ' ').title()
        floor_number = url_parts[3]
        try:
            building = Building.objects.get(name=building_name)
            floor = Floor.objects.get(number=floor_number,
                                      building=building)
        except ObjectDoesNotExist:
            raise Http404
        return floor

    def get_context_data(self, **kwargs):
        context = super(DetailFloor, self).get_context_data(**kwargs)

        requesting_student = Student.objects.get(user=self.request.user)

        students = Student.objects.visible(requesting_student, self.get_object())

        context['students'] = shadowbanning(requesting_student, students)
        # boolean values; helps cut down on if/else block complexity on the template
        context['notOnFloor'] = not(requesting_student in self.get_object())
        context['notInBuilding'] = not(requesting_student in self.get_object().building)
        return context


class DetailRoom(LoginRequiredMixin, DetailView):
    model = Room
    context_object_name = 'room'
    template_name = 'detail_room.html'

    login_url = 'login'

    def get_object(self):
        url_parts = self.request.get_full_path().split('/')
        # ['', 'housing', 'building', 'floor', 'room', ]
        building_name = url_parts[2].replace('-', ' ').title()
        floor_number = url_parts[3]
        room_number = url_parts[4].upper()
        try:
            building = Building.objects.get(name=building_name)
            floor = Floor.objects.get(number=floor_number,
                                      building=building)
            room = Room.objects.get(floor=floor,
                                    number=room_number)
        except ObjectDoesNotExist:
            raise Http404
        return room

    def get_context_data(self, **kwargs):
        context = super(DetailRoom, self).get_context_data(**kwargs)

        requesting_student = Student.objects.get(user=self.request.user)

        students = Student.objects.visible(requesting_student, self.get_object())

        context['students'] = shadowbanning(requesting_student, students)
        context['notOnFloor'] = not(requesting_student in self.get_object().floor)
        context['notInBuilding'] = not(requesting_student in self.get_object().floor.building)
        return context
