# core django imports
from django.contrib.auth.models import User
from django.conf import settings
# third party imports
import requests
# imports from your apps
from .models import Student


def pfinfo(uname):
    base_url = settings.PF_URL
    url = base_url + "basic/all/" + str(uname)
    try:
        metadata = requests.get(url)
        metadata.raise_for_status()
    except requests.exceptions.RequestException as e:
        print e
    else:
        pfjson = metadata.json()
        try:
            name = pfjson['results'][0]['name']
            return name.split(',')
        # if the name is not in peoplefinder, return empty first and last name
        except IndexError:
            return ['', '']


def create_user(tree):

    print 'hello'
    print tree
    username = tree[0][0].text
    print username
    user, user_created = User.objects.get_or_create(username=username)
    print user_created, 'User Created!'

    if user_created:
        print user_created
        user.email = "%s@%s" % (username, settings.ORGANIZATION_EMAIL_DOMAIN)
        print user.email
        user.save()

#        name_list = pfinfo(str(username))
#        print name_list
#        list of empty strings is false
#        first_name = name_list[1].rstrip().split(' ')
#        if it's only a character long
#        if len(first_name) > 1:
#            # no middle initial
#            no_mi = first_name[:-1]
#            user.first_name = ' '.join(no_mi)
#        else:
#            user.first_name = ' '.join(first_name)
#        last_name = name_list[0]
#        user.last_name = last_name
#
#        user.save()
        print user

        new_student = Student.objects.create(user=user)
        new_student.save()
        print new_student

        print "Created user %s!" % username
