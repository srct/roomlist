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

for line in roomNumbers:

    print "}, {\n"
    print "    \"floor\": " + + ",\n"
    print "    \"number\": " + + ",\n"
    print "    \"slug\": \"" + slug_generator() + "\",\n"
    print "    \"room_num\": \"" + + "\",\n"
    print "  },"
    print "  \"model\":\"housing.room\",\n"
    print "  \"pk\":\n"
print "}]"

"""
}, {
  "fields": {
    "floor": 8,
    "number": 204,
    "slug": "8J6yWD",
    "floor_num": "2"
  },
  "model":"housing.floor",
  "pk":44
"""
