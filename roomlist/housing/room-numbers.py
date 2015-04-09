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

print "[{"
# for line in file

pk = 1
curFloorInBuilding = 1
curFloor = 1

for line in roomNumbers:
    if not prog.match('[a-zA-Z]',line):
        print "}, {\n"
        print "    \"floor\": " + curFloor + ",\n"
        print "    \"number\": " + line + ",\n"
        print "    \"room_num\": \"" + line + "\",\n"
        print "    \"slug\": \"" + slug_generator() + "\",\n"
        print "  },"
        print "  \"model\":\"housing.room\",\n"
        print "  \"pk\":\n"
        pk++
print "}]"

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
