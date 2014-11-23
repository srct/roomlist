from django.conf.urls import patterns, include, url

from housing.views import ListBuildings, DetailBuilding, ListRooms, DetailRoom, DetailStudent 
from housing.models import Building, Room, Student 

urlpatterns = patterns('',

    url(r'^student/(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(
            model=Student,
            context_object_name='student',
            template_name='detailStudent.html'),
        name='detailStudent'),

    url(r'^buildings/$',
        ListBuildings.as_view(
            model=Building,
            #paginate_by='10',
            queryset=Building.objects.all(),
            context_object_name='buildings',
            template_name='listBuildings.html'),
        name='listBuildings'),

    url(r'^buildings/(?P<slug>[\w-]+)/$',
        DetailBuilding.as_view(
            model=Building,
            context_object_name='building',
            template_name='detailBuilding.html'),
        name='detailBuilding'),

)
