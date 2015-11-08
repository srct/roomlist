# python manage.py shell < accounts/demo_users.py

# standard libary imports
from __future__ import absolute_import, print_function
# core django imports
from django.contrib.auth.models import User
# imports from your apps
from accounts.models import Student


gmason = User.objects.create_user('gmason', email='gmason@masonlive.gmu.edu',
                                  first_name="George", last_name="Mason",
                                  password='jeffersonsux')
dbond2 = User.objects.create_user('dbond2', email='dbond2@masonlive.gmu.edu',
                                  first_name="James", last_name="Bond",
                                  password='squirrel')
jrouly = User.objects.create_user('jrouly', email='jrouly@masonlive.gmu.edu',
                                  first_name="Jay", last_name="Rouly",
                                  password='doge')
nander13 = User.objects.create_user('nander13', email='jrouly@masonlive.gmu.edu',
                                    first_name="Nander", last_name="Thirteen",
                                    password='@nander13')
spalin = User.objects.create_user('spalin', email='grizzlymama@mccain08.com',
                                  first_name="Sarah", last_name="Palin",
                                  password='youbetcha')
hclinton = User.objects.create_user('hclinton', email='hildawg@mytotallynotsketchysite.us',
                                    first_name="Hillary", last_name="Clinton",
                                    password='')

Student.objects.create(user=gmason)
Student.objects.create(user=dbond2)
Student.objects.create(user=jrouly)
Student.objects.create(user=nander13)
Student.objects.create(user=spalin)
Student.objects.create(user=hclinton)
