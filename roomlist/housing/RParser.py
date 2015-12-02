import re
from housing.models import Building, Floor, Room 

with open('buildingFloors.txt','r') as building_floors:

    for lines in building_floors:
        lines.strip("\n")
        pattern = re.compile("[A-Z a-z]")
        if (pattern.match(lines))
            greg_building = Building.objects.create(name=lines)
            greg_building.save()
        else
            building_floor = Floor.objects.create(number=int(lines), building = greg_building)
            building_floor.save()


with open('roomNunbers.txt','r') as roomnums:

    for (morelines in roomnums):
        morelines.strip("\n")
        pattern = re.compile("[A-Z a-z]")
        if (morelines is "Shenandoah" or morelines is "Aquia" or morelines is "Rappahannock"):
            neighborhood = morelines
        else (pattern.match(morelines)):
            roomBuilding = morelines
            while not(pattern.match(morelines))):
                if (roomBuilding is "Commonwealth" or roomBuilding is "Dominion"):
                    room = Room.objects.create(number=int(morelines), floor=int(morelines[1]))
                    room.save()
                else:
                    room = Room.objects.create(number=int(morelines), floor=int(morelines[0]))
                    room.save()

        