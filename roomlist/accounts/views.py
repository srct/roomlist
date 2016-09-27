# standard library imports
from __future__ import absolute_import, print_function
import random
from distutils.util import strtobool
from operator import attrgetter
from itertools import chain
# core django imports
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import (CreateView, ListView, DetailView, UpdateView,
                                  FormView, DeleteView)
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.forms.widgets import HiddenInput
# third party imports
from braces.views import LoginRequiredMixin, FormValidMessageMixin
from cas.views import login as cas_login
from ratelimit.decorators import ratelimit
# imports from your apps
from .models import Student, Major, Confirmation
from housing.models import Building, Floor, Room
from .forms import StudentUpdateForm
from .student_messages import return_messages


def custom_cas_login(request, *args, **kwargs):
    """If a student has not completed the welcome walkthrough, go there on login."""
    response = cas_login(request, *args, **kwargs)
    # returns HttpResponseRedirect

    if request.user.is_authenticated():

        if not request.user.student.totally_done():

            if not request.user.student.completedName:
                return HttpResponseRedirect(reverse('welcomeName'))
            elif not request.user.student.completedPrivacy:
                return HttpResponseRedirect(reverse('welcomePrivacy'))
            elif not request.user.student.completedMajor:
                return HttpResponseRedirect(reverse('welcomeMajor'))
            elif not request.user.completedSocial:
                return HttpResponseRedirect(reverse('welcomeSocial'))
        else:
            welcome_back = random.choice(return_messages)
            messages.add_message(request, messages.INFO, mark_safe(welcome_back))

    return response


# only two students on the same floor can confirm one another (crowdsourced verification)
def on_the_same_floor(student, confirmer):
    if student == confirmer:
        # Student is confirmer
        return False
    student_floor = student.get_floor()
    confirmer_floor = confirmer.get_floor()
    # room hasn't been set yet
    if (student_floor is None) or (confirmer_floor is None):
        # one Student is None
        return False
    elif not(student_floor == confirmer_floor):
        # not the same floor
        return False
    else:
        return True


def pk_or_none(me, obj):
    if obj is None:
        return None
    else:
        return obj.pk


# details about the student
class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'detailStudent.html'

    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(DetailStudent, self).get_context_data(**kwargs)

        requesting_student = Student.objects.get(user=self.request.user)

        same_floor = on_the_same_floor(self.get_object(), requesting_student)

        flags = Confirmation.objects.filter(confirmer=requesting_student,
                                            student=self.get_object()).count()

        if flags:
            try:
                my_flag = Confirmation.objects.get(confirmer=requesting_student,
                                                   student=self.get_object())
            except Exception as e:
                print("Students are not supposed to be able to make more than one flag per student.")
                print(e)

        def onFloor():
            floor_status = False
            if requesting_student.get_floor() == self.get_object().get_floor():
                floor_status = True
            return floor_status

        def inBuilding():
            floor_status = False
            if requesting_student.get_building() == self.get_object().get_building():
                floor_status = True
            return floor_status

        def shares():
            student_shares = False
            # if the student's privacy is floor and the requesting user is on their floor
            if(self.get_object().privacy == 'floor') and onFloor():
                student_shares = True
            # if the student's privacy is building and the requesting users is
            # on their floor or in their building
            elif(self.get_object().privacy == 'building') and inBuilding():
                student_shares = True
            # if the student's privacy is set to 'student'
            elif(self.get_object().privacy == 'students'):
                student_shares = True
            return student_shares

        context['shares'] = shares()
        context['same_floor'] = same_floor
        context['has_flagged'] = bool(flags)
        if flags:
            context['my_flag'] = my_flag
        return context


# update a student, but FormView to allow name update on same page
class UpdateStudent(LoginRequiredMixin, FormValidMessageMixin, FormView):
    template_name = 'update_student.html'
    form_class = StudentUpdateForm
    login_url = 'login'

    form_valid_message = "Your profile was successfully updated!"

    def get(self, request, *args, **kwargs):

        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]

        if not(url_uname == self.request.user.username):
            return HttpResponseForbidden()
        else:
            return super(UpdateStudent, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UpdateStudent, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)

        form = StudentUpdateForm(initial={'first_name': me.user.first_name,
                                          'last_name': me.user.last_name,
                                          'gender': me.gender,
                                          'show_gender': me.show_gender,
                                          'room': pk_or_none(me, me.room),
                                          'privacy': me.privacy,
                                          'major': pk_or_none(me, me.major),
                                          'graduating_year': me.graduating_year,
                                          'on_campus': me.on_campus, })

        if me.recent_changes() > 2:
            form.fields['room'].widget = HiddenInput()
            form.fields['privacy'].widget = HiddenInput()
            form.fields['on_campus'].widget = HiddenInput()
        else:
            form.fields['room'].widget.user = self.request.user

        # bootstrap
        form.fields['first_name'].widget.attrs['class'] = 'form-control'
        form.fields['last_name'].widget.attrs['class'] = 'form-control'
        form.fields['graduating_year'].widget.attrs['class'] = 'form-control'

        context['my_form'] = form

        return context

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='10/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        #for key, value in request.POST.iteritems():
            #print(key, value)
        return super(UpdateStudent, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        #print("In form valid method!")

        #for key, value in form.data.iteritems():
            #print(key, value)

        current_room = me.room

        # if you somehow got around the hidden widget, you're still outta luck
        if me.recent_changes() > 2:
            form_room = current_room
        else:
            try:
                form_room = Room.objects.get(pk=form.data['room'])
            except:
                form_room = None

        # casts to an integer, 0 or 1
        on_campus = strtobool(form.data.get('on_campus', 'True'))

        # no room if you move off campus
        if not on_campus:
            form_room = None

        # note this is after the 'on campus' check
        if current_room != form_room:
            me.times_changed_room += 1
            Confirmation.objects.filter(student=me).delete()

        me.on_campus = on_campus
        me.room = form_room

        try:
            me.major = Major.objects.get(pk=form.data['major'])
        except:
            me.major = None

        me.user.first_name = form.data['first_name']
        me.user.last_name = form.data['last_name']
        me.gender = form.data.getlist('gender')
        me.show_gender = strtobool(form.data.get('show_gender', 'False'))
        me.privacy = form.data['privacy']
        me.graduating_year = form.data['graduating_year']

        me.user.save()
        me.save()

        return super(UpdateStudent, self).form_valid(form)

    def get_success_url(self):

        if self.request.user.student.recent_changes() == 2:

            messages.add_message(self.request, messages.WARNING, 'To safeguard everyone\'s privacy, you have just one remaining room change for the semester before you\'ll need to send us an email at roomlist@lists.srct.gmu.edu.')

        return reverse('detail_student',
                       kwargs={'slug':self.request.user.username})


# majors pages
class ListMajors(ListView):
    model = Major
    queryset = Major.objects.all().order_by('name')
    context_object_name = 'majors'
    template_name = 'list_majors.html'


class DetailMajor(LoginRequiredMixin, DetailView):
    model = Major
    context_object_name = 'major'
    template_name = 'detail_major.html'

    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(DetailMajor, self).get_context_data(**kwargs)
        requesting_student = Student.objects.get(user=self.request.user)

	# retrieve every room that has a student with the major in question
	neighbourhoods = ("aq", "ra", "sh")
	visible_by_neighbourhood = {}
	for neighbourhood in neighbourhoods:
	    rooms = [
		room
		for room in Room.objects.filter(floor__building__neighbourhood=neighbourhood)
		if room.student_set.filter(major=self.get_object())
	    ]

	    # identify if the student(s) in that room are visible to the requesting student
	    # 'chain' is necessary if there are multiple students in one room with the same major
	    #
	    # we sort each of the lists of students by their username
	    # as elsewhere, this is imperfect if a student changes their display name
	    # this is necessary as a separate step because .visible returns a list type
	    # note we're using '.' instead of '__', because who likes syntactical consistency
	    visible_by_neighbourhood[neighbourhood] = sorted(list(chain(*[
		Student.objects.visible(requesting_student, room)
		for room in rooms
	    ])), key=attrgetter('user.username'))

        # print(visible_by_neighbourhood)

        # see what students are left over (aren't visible)
        hidden = set(Student.objects.filter(major=self.get_object()).order_by('user__username'))
        # print(hidden)
	for visible in visible_by_neighbourhood.values():
            # print('visible', visible)
	    hidden = hidden.difference(set(visible))
            # print(hidden)

	for neighbourhood, visible in visible_by_neighbourhood.iteritems():
	    context['%s_location_visible' % neighbourhood] = visible
        context['location_hidden'] = hidden

        return context


class CreateConfirmation(LoginRequiredMixin, CreateView):
    """Students on the same floor may flag one another.

    This is our attempt at crowdsourced verification."""
    model = Confirmation
    fields = []
    template_name = 'create_confirmation.html'

    login_url = 'login'

    def get(self, request, *args, **kwargs):

        current_url = self.request.get_full_path()
        # [u'', u'accounts', u'student', u'gmason', u'flag', u'']
        url_uname = current_url.split('/')[3]

        confirmer = Student.objects.get(user=self.request.user)
        student = Student.objects.get(slug=url_uname)

        flags = Confirmation.objects.filter(confirmer=confirmer,
                                            student=student).count()

        # you can't flag yourself
        if confirmer == student:
            return HttpResponseForbidden()

        # check that the confirmer is on the floor of the student
        if not on_the_same_floor(student, confirmer):
            return HttpResponseForbidden()

        # check if the confirmer has already flagged the student
        if flags >= 1:
            return HttpResponseForbidden()

        return super(CreateConfirmation, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(CreateConfirmation, self).get_context_data(**kwargs)

        # duplicated code
        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]

        student = Student.objects.get(slug=url_uname)

        context['student'] = student

        return context

    @ratelimit(key='user', rate='10/m', method='POST', block=True)
    @ratelimit(key='user', rate='50/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(CreateConfirmation, self).post(request, *args, **kwargs)

    def form_valid(self, form):

        # duplicated code
        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]

        confirmer = Student.objects.get(user=self.request.user)
        student = Student.objects.get(slug=url_uname)

        form.instance.confirmer = confirmer
        form.instance.student = student

        return super(CreateConfirmation, self).form_valid(form)

    def get_success_url(self):
        # redirect to the flagged student page when saving
        return reverse('detail_student',
                       kwargs={'slug':self.object.student.slug})


class DeleteConfirmation(LoginRequiredMixin, DeleteView):
    model = Confirmation
    template_name = 'delete_confirmation.html'

    login_url = 'login'

    def get(self, request, *args, **kwargs):
        requester = Student.objects.get(user=self.request.user)
        confirmer = self.get_object().confirmer

        if not(requester == confirmer):
            return HttpResponseForbidden()
        else:
            return super(DeleteConfirmation, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('detail_student',
                       kwargs={'slug':self.object.student.slug})
