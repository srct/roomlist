# core django imports
from django.views.generic import DetailView, ListView, CreateView, UpdateView,\
    DeleteView
# third party imports
from braces.views import LoginRequiredMixin
# imports from your apps 
from .models import Building, Floor, Room
from accounts.models import Student


# a list of neighborhoods and their buildings
class ListBuildings(LoginRequiredMixin, ListView):
    model = Building
    queryset = Building.objects.all()
    # paginate_by = 
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
    template_name='detail_building.html'

    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(DetailBuilding, self).get_context_data(**kwargs)
        context['floors'] = Floor.objects.filter(building__name=''+self.get_object().name).order_by('number')
        return context

# this lists the rooms on the floor
class DetailFloor(LoginRequiredMixin, DetailView): 
    model = Floor
    context_object_name = 'floor'
    template_name = 'detail_floor.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailFloor, self).get_context_data(**kwargs)
    
        #requesting_student = Student.objects.get(user=self.request.user)
        requesting_student_filter = Student.objects.filter(user=self.request.user)
        requesting_student = requesting_student_filter[0]

        # if self.request.user is on the floor
        def onFloor():
            floor_status = False
            if requesting_student.get_floor() == self.get_object():
                floor_status = True
            return floor_status

        # if self.request.user is in the building
        def inBuilding():
            building_status = False
            if requesting_student.get_building() == self.get_object().building:
                building_status = True
            return building_status

        rooms = Room.objects.filter(floor=self.get_object()).order_by('number')
        floor_students = []
        for room in rooms:
            if onFloor():
                floor_students.extend(Student.objects.filter(room=room).floor_building_students())
            elif inBuilding():
                floor_students.extend(Student.objects.filter(room=room).building_students())
            else:
                floor_students.extend(Student.objects.filter(room=room).students())

        context['students'] = floor_students
        context['notOnFloor'] = not onFloor()
        context['notInBuilding'] = not inBuilding()
        return context

class DetailRoom(LoginRequiredMixin, DetailView):
    model = Room
    context_object_name = 'room'
    template_name='detail_room.html'

    def get_context_data(self, **kwargs):
        context = super(DetailRoom, self).get_context_data(**kwargs)

        #requesting_student = Student.objects.get(user=self.request.user)
        requesting_student_filter = Student.objects.filter(user=self.request.user)
        requesting_student = requesting_student_filter[0]

        # if self.request.user is on the floor
        def onFloor():
            floor_status = False
            if requesting_student.get_floor() == self.get_object().floor:
                floor_status = True
            return floor_status

        # if self.request.user is in the building
        def inBuilding():
            building_status = False
            if requesting_student.get_building() == self.get_object().floor.building:
                building_status = True
            return building_status

        if onFloor():
             students = Student.objects.filter(room=self.get_object()).floor_building_students()
        elif inBuilding():
             students = Student.objects.filter(room=self.get_object()).building_students()
        else:
             students = Student.objects.filter(room=self.get_object()).students()

        context['students'] = students
        context['notOnFloor'] = not onFloor()
        context['notInBuilding'] = not inBuilding()

        return context

    login_url = '/'

# deleted 'UpdateRoom' view-- that will be handled on the user's page
