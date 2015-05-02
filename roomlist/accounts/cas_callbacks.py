# core django imports
from django.contrib.auth.models import User
from django.conf import settings
# third party imports
import requests
# imports from your apps
from .models import Student


def pfinfo(uname):
    base_url = "http://peoplefinder.b1.akshaykarthik.com/"
    url = base_url + "basic/all/" + str(uname)
    try:
        metadata = requests.get(url)
        metadata.raise_for_status()
    except requests.exceptions.RequestException as e:
        print e
    else:
        pfjson = metadata.json()
        name = pfjson['results'][0]['name']
        return name.split(',')

def create_user(tree):

    username = tree[0][0].text
    user, user_created = User.objects.get_or_create(username=username)

    if user_created:
        user.email = "%s@%s" % (username, settings.ORGANIZATION_EMAIL_DOMAIN)

        name_list = pfinfo(username)
        user.first_name = name_list[1].rstrip()
        user.last_name = name_list[0]

        user.save()

        new_student = Student.objects.create(user=user)
        new_student.save()

        print("Created user %s!" % username)
