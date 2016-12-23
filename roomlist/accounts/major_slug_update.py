# python manage.py shell < accounts/major_slug_update.py

# this script updates slugs from a previous release of django from random strings
# to a slugified version of the object's name, e.g. the name of the major

# standard library imports
from __future__ import absolute_import, print_function, unicode_literals

from accounts.models import Major

majors = Major.objects.all()

for major in majors:
    print(major.name)
    print(major.slug)
    major.save()
    print(major.slug)
