from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from housing.models import Building, Room
from accounts.models import Student

from braces.views import LoginRequiredMixin

# a list of neighborhoods and their buildings
class ListBuildings(LoginRequiredMixin, ListView):
    model = Building
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ListBuildings, self).get_context_data(**kwargs)
        context['rappahannock'] = Building.objects.filter(neighbourhood='ra')
        context['shenandoah'] = Building.objects.filter(neighbourhood='sh')
        context['aquia'] = Building.objects.filter(neighbourhood='aq')
        return context

# building floors, other information
class DetailBuilding(LoginRequiredMixin, DetailView):
    model = Building
    context_object_name = 'building'
    template_name='detailBuilding.html'

    def get_context_data(self, **kwargs):
        context = super(DetailBuilding, self).get_context_data(**kwargs)
        context['floors'] = Floor.objects.filter(building__name=''+self.get_object().name_.order_by('-number')
        return context

    login_url = '/'

# this lists the rooms on the floor
class DetailFloor(LoginRequiredMixin, DetailView):
    model = Floor
    context_object_name = 'floor'
    template_name = detail_floor.html

    def get_context_data(self, **kwargs):
        context = super(DetailFloor, self):
        context['rooms'] = Room.objects.filter(floor=self.get_object()).order_by('-number')
        return context

    login_url = '/'

# this lists students in a room
class DetailRoom(LoginRequiredMixin, ListView):
    model = Room

    def get_context_data(self, **kwargs):
        context = super(DetailRoom, self):
#        context['students'] = 
        return context

    login_url = '/'

# deleted 'updateroom' view-- that will be handled on the user's page
