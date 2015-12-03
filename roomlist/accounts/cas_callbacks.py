# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib import messages
# third party imports
import requests
# imports from your apps
from .models import Student, Major
from settings.slack import slack_post


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
        metadata = requests.get(url, timeout=5)
        print("Retrieving information from the peoplefinder api.")
        metadata.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Cannot resolve to peoplefinder api:", e)
        print("Returning empty user info tuple.")
        return ([u'', u''], u'')
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
            print("Name not found in peoplefinder.")
            name = [u'', u'']
            major = u''
            final_tuple = (name, major)
            return final_tuple
        # if there's no major, just return that as an empty string
        except KeyError:
            print("Major not found in peoplefinder.")
            final_tuple = (name, u'')
            return final_tuple
        except Exception as e:
            print("Unknown peoplefinder error:", e)
            print("Returning empty user info tuple.")
            return ([u'', u''], u'')


def create_user(tree):

    print("Parsing CAS information.")
    try:
        username = tree[0][0].text
        user, user_created = User.objects.get_or_create(username=username)
    except Exception as e:
        print("CAS callback unsuccessful:", e)

    # error handling in pfinfo function
    info_tuple = pfinfo(username)

    try:
        if user_created:
            print("Created user object %s." % username)

            # notify developers of user signup milestones
            num_users = User.objects.all().count()
            if num_users % 50:
                message = "Congratulations! We've passed %d user registrations!" % num_users
                slack_post(text=message,
                           channel='#roomlist',
                           username='Roomlist User Milestones',
                           icon_emoji=':tada:')

            # set and save the user's email
            email_str = "%s@%s" % (username, settings.ORGANIZATION_EMAIL_DOMAIN)
            user.email = email_str
            # Password is a required User object field, though doesn't matter for our
            # purposes because all user auth is handled through CAS, not Django's login.
            user.password = 'cas_used_instead'
            user.save()
            print("Added user's email, %s." % email_str)

            info_name = info_tuple[0]
            # a list of empty strings is False
            if not info_name:
                user.first_name = info_name[0]
                user.last_name = info_name[1]
                user.save()
                print("Added user's name, %s %s." % (info_name[0], info_name[1]))
            else:
                print("Unable to add user's name.")

            print("User object creation process completed.")

        else:
            print("User object already exists.")

        try:
            Student.objects.get(user=user)
            print("Student object already exists.")

        except ObjectDoesNotExist:
            new_student = Student.objects.create(user=user)
            new_student.save()
            print("Created student object.")

            major_name = info_tuple[1]
            try:
                major_obj = Major.objects.get(name__contains=major_name)
                new_student.major = major_obj
                new_student.save()
                print("Added student's major, %s." % major_name)
            # ironically, 'Computer Science' returns a MultipleObjectsReturned exception
            # also Major.DoesNotExist Error, but the handling for both is the same...
            except:
                print("Unable to add student's major.")
            try:
                new_student.original_first_name = info_name[0]
                new_student.original_last_name = info_name[1]
                print("Added student's original name for later reference.")
            except:
                print("Unable to add student's original name for later reference.")
            try:
                new_student.original_major = major_obj
                new_student.save()
                print("Added student's original major, %s, for later reference." % major_name)
            except:
                print("Unable to add student's original major for later reference.")

            print("Student object creation process completed.")

        print("CAS callback successful.")
    except Exception as e:
        print("Unhandled user creation error:", e)
        # mail the administrators
