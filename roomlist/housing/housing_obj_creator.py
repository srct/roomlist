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

# building name, neighborhood
mason_housing = {'Adams': 'sh',
                 'Apartment 1': 'aq',
                 'Apartment 2': 'aq',
                 'Apartment 3': 'aq',
                 'Apartment 4': 'aq',
                 'Apartment 5': 'aq',
                 'Apartment 6': 'aq',
                 'Apartment 7': 'aq',
                 'Apartment 8': 'aq',
                 'Apartment 9': 'aq',
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
                 'Liberty Square': 'sh',  # wing letters precede room numbers
                 'Madison': 'sh',
                 'Monroe': 'sh',
                 'Northern Neck': 'ra',
                 'Piedmont': 'ra',
                 'Potomac Heights': 'sh',
                 'Rogers': 'aq',
                 'Roosevelt': 'sh',
                 'Sandbridge': 'ra',
                 'Tidewater': 'ra',
                 'Truman': 'sh',
                 'Washington': 'sh',
                 'Whitetop': 'aq',
                 'Wilson': 'sh', }

# Townhouses -- really whacky naming
# Beacon Hall -- graduate students
# Mason Global Center -- international students

start_time = datetime.now()
print("Creating buildings...")

new_buildings = 0

for building_name, neighborhood in mason_housing.iteritems():
    my_building, building_created = Building.objects.get_or_create(name=building_name,
                                                                   neighbourhood=neighborhood)
    if not building_created:
        print(my_building)
    else:
        my_building.save()
        new_buildings += 1
        print(my_building, "(NEW!)")

print("Created %d new buildings, %d buildings total." % (new_buildings,
                                                         Building.objects.all().count()))
print("Creating floors...")

new_floors = 0

with open('housing/building_floors.txt') as buildings:
    for line in buildings:
        line = line.strip()
        if re.match('^[a-z A-Z]*( {1}\d)?$', line):
            current_building = Building.objects.get(name=line)
            print(current_building)
        else:
            my_floor, floor_created = Floor.objects.get_or_create(number=line,
                                                                  building=current_building)
            if floor_created:
                my_floor.save()
                new_floors += 1

print("Created %d new floors, %d floors total." % (new_floors,
                                                   Floor.objects.all().count()))
print("Creating rooms...")

new_rooms = 0

with open('housing/building_rooms.txt') as rooms:
    for line in rooms:
        line = line.strip()
        if re.match('^[a-z A-Z]*( {1}\d)?$', line):
            current_building = Building.objects.get(name=line)
            print(current_building)
        else:
            if current_building.name in ('Commonwealth', 'Dominion', 'Liberty Square'):
                my_floor = Floor.objects.get(building=current_building, number=line[1])
            else:
                my_floor = Floor.objects.get(building=current_building, number=line[0])
            my_room, room_created = Room.objects.get_or_create(floor=my_floor,
                                                               number=line)
            if room_created:
                new_rooms += 1
                my_room.save()

print("Created %d new rooms, %d rooms total." % (new_rooms, Room.objects.all().count()))
end_time = datetime.now()
total_time = end_time - start_time
print("Elapsed time:", total_time)
