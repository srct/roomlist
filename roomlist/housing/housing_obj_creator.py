# python manage.py shell < housing/housing_obj_creator.py

# Please note this script is meant to be run when the database is entirely devoid of
# any housing app objects. Error handling is essentially nonexistent.

# standard library imports
from __future__ import absolute_import, print_function
import re
from datetime import datetime
# imports from your apps
from housing.models import Building, Floor, Room

# check if there are buildings already in the database
# check if there are floors already in the database
# check if there are rooms already in the database

# fail if there is already stuff there?

# building name, neighborhood
mason_housing = { 'Adams': 'sh',
                  'Amherst': 'ra',
                  'Blue Ridge': 'ra',
                  'Brunswick': 'ra',
                  'Carroll': 'ra',
                  'Commonwealth': 'ra',  # weird floor numbers, use [1] instead of [0]
                  'Dickenson': 'ra',
                  'Dominion': 'ra',  # ditto Commonwealth
                  'Eastern Shore': 'ra',
                  'Essex': 'ra',
                  'Franklin': 'ra',
                  'Grayson': 'ra',
                  'Hampton Roads': 'ra',
                  'Harrison': 'sh',
                  'Jackson': 'sh',
                  'Jefferson': 'sh',
                  'Kennedy': 'sh',
                  'Lincoln': 'sh',
                  'Madison': 'sh',
                  'Monroe': 'sh',
                  'Northern Neck': 'ra',
                  'Potomac Heights': 'sh',
                  'Rogers': 'aq',
                  'Roosevelt': 'sh',
                  'Sandbridge': 'ra',
                  'Truman': 'sh',
                  'Washington': 'sh',
                  'Whitetop': 'aq',
                  'Wilson': 'sh', }

# Student Apartments -- multiple buildings
# Townhouses -- multiple buildings
# Piedmont -- broken off-by-one blueprint
# Tidewater -- broken off-by-one blueprint
# Beacon Hall -- graduate students
# Liberty Square -- Weird letters in name
# Mason Global Center -- international students

start_time = datetime.now()
print("Creating buildings...")

for building_name, neighborhood in mason_housing.iteritems():
    my_building = Building.objects.create(name=building_name, neighbourhood=neighborhood)
    print(my_building)
    my_building.save()

print("Created %d buildings." % Building.objects.all().count())
print("Creating floors...")

with open('housing/buildingFloors.txt') as buildings:
    for line in buildings:
        line = line.rstrip('\n')
        if re.match('[a-z A-z]', line):
            print(line)
            current_building = Building.objects.get(name=line)
        else:
            my_floor = Floor.objects.create(number=int(line), building=current_building)
            my_floor.save()

print("Created %d floors." % Floor.objects.all().count())
print("Creating rooms...")

with open('housing/building_rooms.txt') as rooms:
     for line in rooms:
         line = line.rstrip('\n')
         if re.match('[a-z A-Z]', line):
             current_building = Building.objects.get(name=line)
             print(current_building)
         else:
             if current_building.name in ('Commonwealth', 'Dominion'):
                 my_floor = Floor.objects.get(building=current_building, number=int(line[1]))
             else:
                 my_floor = Floor.objects.get(building=current_building, number=int(line[0]))
             my_room = Room.objects.create(floor=my_floor, number=int(line))
             my_room.save()

print("Created %d rooms." % Room.objects.all().count())
end_time = datetime.now()
total_time = end_time - start_time
print("Elapsed time:", total_time)
