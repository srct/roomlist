# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import (CreateView, ListView, DetailView, UpdateView,
                                  FormView, DeleteView)
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.safestring import mark_safe
# third party imports
from braces.views import LoginRequiredMixin
from cas.views import login as cas_login
from ratelimit.decorators import ratelimit
# imports from your apps
from .models import Student, Major, Room, Confirmation
from .forms import StudentUpdateForm, WelcomeNameForm


not_started = """Welcome to SRCT Roomlist! <a href="%s">Click here</a> to walk through
                 your profile setup."""

# 1 or 2
started = """Welcome back to SRCT Roomlist! It looks like you're not quite finished with
             setting up your profile. <a href="%s">Click here</a> to return to your
             welcome walkthrough."""

# 3
almost = """Welcome back to SRCT Roomlist! It looks like you're almost finished
            with setting up your profile. <a href="%s">Click here</a> to return
            to the last page of your welcome walkthrough."""

# walkthrough finished but Room is None
no_room = """It looks like you haven't set your room yet. Head to <a href="%s"> your
             settings page</a> to get that taken care of."""


def custom_cas_login(request, *args, **kwargs):
    response = cas_login(request, *args, **kwargs)
    # returns HttpResponseRedirect
    if request.user.is_authenticated():

        if request.user.student.completedName is False:
            rendered_url = reverse('welcomeName', args=[request.user.username])
            add_url = not_started % rendered_url
            messages.add_message(request, messages.INFO, mark_safe(add_url))

        elif request.user.student.completedPrivacy is False:
            rendered_url = reverse('welcomePrivacy', args=[request.user.username])
            add_url = started % rendered_url
            messages.add_message(request, messages.INFO, mark_safe(add_url))

        elif request.user.student.completedMajor is False:
            rendered_url = reverse('welcomeMajor', args=[request.user.username])
            add_url = started % rendered_url
            messages.add_message(request, messages.INFO, mark_safe(add_url))

        elif request.user.student.completedName is False:
            rendered_url = reverse('welcomeSocial', args=[request.user.username])
            add_url = started % rendered_url
            messages.add_message(request, messages.INFO, mark_safe(add_url))

        elif request.user.student.room is None:
            rendered_url = reverse('updateStudent', args=[request.user.username])
            add_url = started % rendered_url
            messages.add_message(request, messages.INFO, mark_safe(add_url))
        # eventually add a reminder if the privacy is set to students
        # one in ten change will display a reminder and link to change

    return response


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


# details about the student
class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'detailStudent.html'

    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(DetailStudent, self).get_context_data(**kwargs)

        # requesting_student = Student.objects.get(user=self.request.user)
        requesting_student_filter = Student.objects.filter(user=self.request.user)
        requesting_student = requesting_student_filter[0]

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


class DetailCurrentStudent(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'detailStudent.html'

    login_url = 'login'

    def get_object(self):
        return get_object_or_404(Student, pk=self.request.session['_auth_user_id'])


# changeable student settings
class DetailStudentSettings(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'studentSettings.html'

    login_url = 'login'


class DetailCurrentStudentSettings(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'studentSettings.html'

    login_url = 'login'

    def get_object(self):
        return get_object_or_404(Student, pk=self.request.session['_auth_user_id'])


# update a student, but FormView to allow name update on same page
class UpdateStudent(LoginRequiredMixin, FormView):
    template_name = 'updateStudent.html'
    form_class = StudentUpdateForm
    login_url = 'login'

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

        def pk_or_none(me, obj):
            if obj is None:
                return None
            else:
                return obj.pk

        form = StudentUpdateForm(initial={'first_name': me.user.first_name,
                                        'last_name': me.user.last_name,
                                        'gender': me.gender,
                                        'room': pk_or_none(me, me.room),
                                        'privacy': me.privacy,
                                        'major': pk_or_none(me, me.major),
                                        'graduating_year' : me.graduating_year,})
        context['my_form'] = form
        return context

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        me.user.first_name = form.data['first_name']
        me.user.last_name = form.data['last_name']
        me.gender = form.data.getlist('gender')
        me.room = Room.objects.get(pk=form.data['room'])
        me.privacy = form.data['privacy']
        me.major = Major.objects.get(pk=form.data['major'])
        me.graduating_year = form.data['graduating_year']


        me.user.save()
        me.save()

        return super(UpdateStudent, self).form_valid(form)

    def get_success_url(self):
        return reverse('detail_student',
                       kwargs={'slug':self.request.user.username})

# welcome pages
class WelcomeName(LoginRequiredMixin, FormView):
    template_name = 'welcome_name.html'
    form_class = WelcomeNameForm
    login_url = 'login'

    def get(self, request, *args, **kwargs):

        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]

        if not(url_uname == self.request.user.username):
            return HttpResponseForbidden()
        else:
            return super(WelcomeName, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WelcomeName, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)

        form = WelcomeNameForm(initial={'first_name': me.user.first_name,
                                        'last_name': me.user.last_name,
                                        'gender': me.gender, })
        context['my_form'] = form
        return context
        
    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        me.user.first_name = form.data['first_name']
        me.user.last_name = form.data['last_name']

        me.gender = form.data.getlist('gender')

        me.completedName = True

        me.user.save()
        me.save()

        return super(WelcomeName, self).form_valid(form)

    def get_success_url(self):
        return reverse('welcomePrivacy',
                       kwargs={'slug':self.request.user.username})


class WelcomePrivacy(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ['room', 'privacy', ]
    context_object_name = 'student'
    template_name = 'welcome_privacy.html'

    login_url = 'login'

    def get(self, request, *args, **kwargs):

        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]

        if not(url_uname == self.request.user.username):
            return HttpResponseForbidden()
        else:
            return super(WelcomePrivacy, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.obj = self.get_object()

        self.obj.completedPrivacy = True
        self.obj.save()

        return super(WelcomePrivacy, self).form_valid(form)

    def get_success_url(self):
        return reverse('welcomeMajor',
                       kwargs={'slug':self.request.user.username})


class WelcomeMajor(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ['major', 'graduating_year', ]
    context_object_name = 'student'
    template_name = 'welcome_major.html'

    login_url = 'login'

    def get(self, request, *args, **kwargs):

        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]

        if not(url_uname == self.request.user.username):
            return HttpResponseForbidden()
        else:
            return super(WelcomeMajor, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.obj = self.get_object()

        self.obj.completedMajor = True
        self.obj.save()

        return super(WelcomeMajor, self).form_valid(form)

    def get_success_url(self):
        return reverse('welcomeSocial',
                       kwargs={'slug':self.request.user.username})


class WelcomeSocial(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'welcome_social.html'

    login_url = 'login'

    # push to the message queue

    def get(self, request, *args, **kwargs):

        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]

        if not(url_uname == self.request.user.username):
            return HttpResponseForbidden()
        else:
            return super(WelcomeSocial, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.obj = self.get_object()

        self.obj.completedSocial = True
        self.obj.save()

        return super(WelcomeSocial, self).form_valid(form)

    def get_success_url(self):
        return reverse('detail_student',
                       kwargs={'slug':self.request.user.username})


# majors pages
class ListMajors(LoginRequiredMixin, ListView):
    model = Major
    queryset = Major.objects.all().order_by('name')
    context_object_name = 'majors'
    template_name = 'list_majors.html'

    login_url = 'login'


class DetailMajor(LoginRequiredMixin, DetailView):
    model = Major
    context_object_name = 'major'
    template_name = 'detail_major.html'

    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(DetailMajor, self).get_context_data(**kwargs)
        me = Student.objects.get(user=self.request.user)

        students = Student.objects.filter(major=self.get_object()).order_by('room__floor__building__name', 'user__last_name', 'user__first_name')

        def onFloor(me, student):
            floor_status = False
            if me.get_floor() == student.get_floor():
                floor_status = True
            return floor_status

        def inBuilding(me, student):
            floor_status = False
            if me.get_building() == student.get_building():
                floor_status = True
            return floor_status

        aq_location_visible = []
        ra_location_visible = []
        sh_location_visible = []
        location_hidden = []

        aq_students = students.filter(room__floor__building__neighbourhood='aq')

        for student in aq_students:
            if student.privacy == u'students':
                aq_location_visible.append(student)
            elif (student.privacy == u'building') and inBuilding(me, student):
                aq_location_visible.append(student)
            elif (student.privacy == u'floor') and onFloor(me, student):
                aq_location_visible.append(student)
            else:
                location_hidden.append(student)

        ra_students = students.filter(room__floor__building__neighbourhood='ra')

        for student in ra_students:
            if student.privacy == u'students':
                ra_location_visible.append(student)
            elif (student.privacy == u'building') and inBuilding(me, student):
                ra_location_visible.append(student)
            elif (student.privacy == u'floor') and onFloor(me, student):
                ra_location_visible.append(student)
            else:
                location_hidden.append(student)

        sh_students = students.filter(room__floor__building__neighbourhood='sh')

        for student in sh_students:
            if student.privacy == u'students':
                sh_location_visible.append(student)
            elif (student.privacy == u'building') and inBuilding(me, student):
                sh_location_visible.append(student)
            elif (student.privacy == u'floor') and onFloor(me, student):
                sh_location_visible.append(student)
            else:
                location_hidden.append(student)

        context['aq_location_visible'] = aq_location_visible
        context['ra_location_visible'] = ra_location_visible
        context['sh_location_visible'] = sh_location_visible
        context['location_hidden'] = location_hidden

        return context


class CreateConfirmation(LoginRequiredMixin, CreateView):
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

    def form_valid(self, form):

        # duplicated code
        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]

        confirmer = Student.objects.get(user=self.request.user)
        student = Student.objects.get(slug=url_uname)

        form.instance.confirmer = confirmer
        form.instance.student = student

        return super(CreateConfirmation, self).form_valid(form)

    @ratelimit(key='user', rate='10/m', method='POST', block=True)
    @ratelimit(key='user', rate='50/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(CreateConfirmation, self).post(request, *args, **kwargs)

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
