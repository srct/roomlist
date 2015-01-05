from django.conf.urls import patterns, include, url

from housing.views import ListBuildings, DetailBuilding, ListRooms, DetailRoom
from housing.models import Building, Room

urlpatterns = patterns('',

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
            slug_field='slug__iexact',
            context_object_name='building',
            template_name='detailBuilding.html'),
        name='detailBuilding'),

)
