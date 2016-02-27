# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.views.generic import DetailView, ListView
# third party imports
from braces.views import LoginRequiredMixin
# imports from your apps
from .models import Building, Floor, Room
from accounts.models import Student


# this should be written in cache, to be entirely honest
def shadowbanning(me, other_people):
    # start with only students who are actually blocking anyone
    blockers = [student for student in Student.objects.exclude(blocked_kids__exact='')]
    # of those students, collect the ones that block *you*
    blocks_me = [student
                 for student in blockers
                 if me in student.blocked_kids.all()]
    if len(blocks_me):
        student_safety = list(set(other_people) - set(blocks_me))
        return student_safety
    else:
        return other_people


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
        # [u'', u'housing', u'building',]
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
        # [u'', u'housing', u'building', u'floor', ]
        building_name = url_parts[2].replace('-', ' ').title()
        floor_number = int(url_parts[3])
        building = Building.objects.get(name=building_name)
        floor = Floor.objects.get(number=floor_number,
                                  building=building)
        return floor

    def get_context_data(self, **kwargs):
        context = super(DetailFloor, self).get_context_data(**kwargs)

        requesting_student = Student.objects.get(user=self.request.user)

        students = Student.objects.visible(requesting_student, self.get_object())
        notOnFloor = not(requesting_student in self.get_object())
        notInBuilding = not(requesting_student in self.get_object().building)

        context['students'] = shadowbanning(requesting_student, students)
        context['notOnFloor'] = shadowbanning(requesting_student, notOnFloor)
        context['notInBuilding'] = shadowbanning(requesting_student, notInBuilding)
        return context


class DetailRoom(LoginRequiredMixin, DetailView):
    model = Room
    context_object_name = 'room'
    template_name = 'detail_room.html'

    def get_object(self):
        url_parts = self.request.get_full_path().split('/')
        # [u'', u'housing', u'building', u'floor', u'room', ]
        building_name = url_parts[2].replace('-', ' ').title()
        floor_number = int(url_parts[3])
        room_number = int(url_parts[4])
        building = Building.objects.get(name=building_name)
        floor = Floor.objects.get(number=floor_number,
                                  building=building)
        room = Room.objects.get(floor=floor,
                                number=room_number)
        return room

    def get_context_data(self, **kwargs):
        context = super(DetailRoom, self).get_context_data(**kwargs)

        requesting_student = Student.objects.get(user=self.request.user)

        students = Student.objects.visible(requesting_student, self.get_object())
        notOnFloor = not(requesting_student in self.get_object().floor)
        notInBuilding = not(requesting_student in self.get_object().floor.building)

        context['students'] = shadowbanning(requesting_student, students)
        context['notOnFloor'] = shadowbanning(requesting_student, notOnFloor)
        context['notInBuilding'] = shadowbanning(requesting_student, notInBuilding)
        return context
