import requests
from bs4 import BeautifulSoup
import re
#import io

try:
    page = requests.get('http://catalog.gmu.edu/content.php?catoid=25&navoid=4959')
    page.raise_for_status()

except requests.exceptions.RequestException as e:
    print e

else:
    programs = BeautifulSoup(page.content)

    lists = programs.find_all('li')

    program_names = []

    for line in lists:
        program_title = line.a.string
        if re.search(r'(BA|BS|BAS|BFA|BSW|BSN|BSEd|BM|BIS)$', program_title):
            program_names.append(program_title)

    fixtures = open('major_fixtures.json', 'w')

    fixtures.write('[{\n')

    # the last item is an edge case the way the brackets work
    for place in range(len(program_names)-1):

        fixtures.write('  "fields": {\n    "name": "' + program_names[place] + '"\n')
        fixtures.write('  },\n  "model": "accounts.major",\n')
        fixtures.write('  "pk": ' + str(place + 1) + '\n}, {\n')

    # the last item in the list
    fixtures.write('  "fields": {\n    "name": "' + program_names[-1] + '"\n')
    fixtures.write('  },\n  "model": "accounts.major",\n')
    fixtures.write('  "pk": ' + str(len(program_names)) + '\n')

    fixtures.write('}]\n')

    fixtures.close()
