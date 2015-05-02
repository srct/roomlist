# standard library imports
import io
import string
import random
import re

# from stackoverflow https://stackoverflow.com/questions/2257441/
def slug_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# regex to separate out building names and room numbers
def building_or_room(line):


    return False

def get_floor_num(line):
    return line[0]

roomNumbers = open('room-numbers', 'r')

print("[{")
# for line in file

pk = 1
curFloor = 0
curFloorInBuilding = 1

for line in roomNumbers:
    line = line.rstrip('\n')
    if re.match('[a-zA-Z]',line):
        curFloor += 1
        curFloorInBuilding = 1
    else:
        if int(float(get_floor_num(line))) > curFloorInBuilding:
            curFloor += 1
            curFloorInBuilding += 1
        print("}, {\"fields\": {")
        print("    \"floor\": " + str(curFloor) + ",")
        print("    \"number\": " + str(line) + ",")
        print("    \"room_num\": \"" + str(line) + "\",")
        print("    \"slug\": \"" + slug_generator() + "\"")
        print("  },")
        print("  \"model\":\"housing.room\",")
        print("  \"pk\":" + str(pk))
        pk = pk + 1
print("}]")

"""
  "fields": {
    "floor": 1,
    "created": "2015-04-09T19:56:59.594Z",
    "number": 101,
    "modified": "2015-04-09T19:56:59.598Z",
    "room_num": "101",
    "slug": "G4xTdX"
  },
  "model": "housing.room",
  "pk": 1
}, {
"""
