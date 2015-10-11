# core django imports
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
# third party imports
import requests
# imports from your apps
from .models import Student, Major


def pfparse(pf_name_result):
    # name comes in format of Anderson, Nicholas J
    name_list = pf_name_result.split(',')
    # there's random whitespace with the first name
    first_name_section = name_list[1].strip()
    # check if there's a middle initial
    mi_q = first_name_section.split(' ')
    # make sure that the additional elements aren't multiple names
    if len(mi_q[-1]) == 1:
        first_name = ' '.join(mi_q[:-1])
    else:
        first_name = first_name_section
    new_name_list = [first_name, name_list[0]]
    return new_name_list


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
            if len(pfjson['results']) == 1:
                name_str = pfjson['results'][0]['name']
                name = pfparse(name_str)
                major = pfjson['results'][0]['major']
                # could conceivably throw a key error
                final_tuple = (name, major)
                return final_tuple
            else:
                name_str = pfjson['results'][1]['name']
                name = pfparse(name_str)
                major = pfjson['results'][1]['major']
                # could conceivably throw a key error
                final_tuple = (name, major)
                return final_tuple
        # if the name is not in peoplefinder, return empty first and last name
        except IndexError:
            name = [u'', u'']
            major = u''
            final_tuple = (name, major)
            return final_tuple
        # if there's no major, just return that as an empty string
        except KeyError:
            final_tuple = (name, u'')
            return final_tuple


def create_user(tree):

    print "Parsing CAS information."
    username = tree[0][0].text
    user, user_created = User.objects.get_or_create(username=username)

    if user_created:
        print "Created user object %s." % username
 
        # set and save the user's email
        email_str = "%s@%s" % (username, settings.ORGANIZATION_EMAIL_DOMAIN)
        user.email = email_str
        user.save()
        print "Added user's email, %s." % email_str

        info_tuple = pfinfo(username)
        info_name = info_tuple[0]
        # a list of empty strings is False
        if not info_name:
            user.first_name = info_name[0]
            user.last_name = info_name[1]
            user.save()
            print "Added user's name, %s %s." % (info_name[0], info_name[1])

        new_student = Student.objects.create(user=user)
        new_student.save()
        print "Created student object."

        major_name = info_tuple[1]
        try:
            major_obj = Major.objects.get(name__contains=major_name)
            new_student.major = major_obj
            new_student.save()
            print "Added student's major, %s." % major_name
        # ironically, 'Computer Science' returns a MultipleObjectsReturned exception
        # also Major.DoesNotExist Error, but the handling for both is the same...
        except:
            pass
            
        print "User creation process completed."

    print "CAS callback successful."
