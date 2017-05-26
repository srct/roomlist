# standard library imports
from __future__ import absolute_import, print_function
from distutils.util import strtobool
from collections import OrderedDict
from itertools import groupby
# core django imports
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.views.generic import CreateView, ListView, DetailView, FormView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.forms.widgets import HiddenInput
from django.core.mail import get_connection
from django.core.exceptions import ObjectDoesNotExist
# third party imports
from braces.views import LoginRequiredMixin, FormValidMessageMixin
from ratelimit.decorators import ratelimit
# imports from your apps
from .models import Student, Major, Confirmation
from .forms import StudentUpdateForm, FarewellFeedbackForm
from housing.models import Room
from core.utils import (shadowbanning, on_the_same_floor, pk_or_none, create_email,
                        no_nums)
from core.views import StudentContextMixin


# details about the student
class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'detail_student.html'

    login_url = 'login'

    def get(self, request, *args, **kwargs):

        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]
        try:
            detailed_student = Student.objects.get(user__username=url_uname)
        except ObjectDoesNotExist:
            raise Http404

        if (detailed_student in self.request.user.student.blocked_kids.all()):
            raise Http404
        else:
            return super(DetailStudent, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailStudent, self).get_context_data(**kwargs)

        requesting_student = self.request.user.student

        same_floor = on_the_same_floor(self.get_object(), requesting_student)

        flags = Confirmation.objects.filter(confirmer=requesting_student,
                                            student=self.get_object()).count()

        if flags:
            try:
                my_flag = Confirmation.objects.get(confirmer=requesting_student,
                                                   student=self.get_object())
            # students are not supposed to be able to make more than one flag per student
            except Exception as e:
                print(e)

        # recognizably too complex
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
        try:
            student = Student.objects.get(user__username=url_uname)
        except ObjectDoesNotExist:
            raise Http404

        if not(url_uname == self.request.user.username):
            return HttpResponseRedirect(reverse('update_student',
                                                kwargs={'slug': self.request.user.username}))
        else:
            return super(UpdateStudent, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(UpdateStudent, self).get_initial()

        me = self.request.user.student
        majors = [pk_or_none(me, major) for major in me.major.all()]

        initial = {'first_name': me.user.first_name,
                   'last_name': me.user.last_name,
                   'gender': me.gender,
                   'show_gender': me.show_gender,
                   'room': pk_or_none(me, me.room),
                   'privacy': me.privacy,
                   'blocked_kids': me.blocked_kids.all(),
                   'major': majors,
                   'graduating_year': me.graduating_year,
                   'on_campus': me.on_campus, }

        return initial

    def get_form(self):
        form = super(UpdateStudent, self).get_form(StudentUpdateForm)

        me = self.request.user.student

        form.fields['blocked_kids'].queryset = Student.objects.exclude(user=self.request.user)
        form.fields['room'].widget.user = self.request.user

        if me.recent_changes() > 2:
            form.fields['room'].required = False
            form.fields['room'].widget = HiddenInput()
            form.fields['on_campus'].required = False
            form.fields['on_campus'].widget = HiddenInput()

        # RAs and RDs cannot move off campus
        if me.is_staff():
            form.fields['on_campus'].required = False
            form.fields['on_campus'].disabled = True

        return form

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='10/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        # for key, value in request.POST.iteritems():
        #     print(key, value)
        return super(UpdateStudent, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        me = self.request.user.student

        # print("In form valid method!")

        # for key, value in form.data.iteritems():
        #     print(key, value)

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

        # if you don't live on campus you can't limit yourself to a nonexistent
        # floor or room
        if not(me.on_campus):
            me.privacy = 'students'
        else:
            me.privacy = form.data['privacy']

        # if you are an RA or an RD, you live on campus
        if me.is_staff():
            me.on_campus = True

        try:
            # in case someone disabled the js, limit processing to only the first
            # two majors passed by the user
            # we also eliminate the potential a student manipulates the form to
            # pass in two majors of the same type by casting to a set
            form_major_pks = set(form.data.getlist('major')[:2])
            # retrieve the major objects from the list of pk strings
            form_majors = [Major.objects.get(pk=pk) for pk in form_major_pks]
            # print(form_majors)
            # iterate over a student's current majors
            for current_major in me.major.all():
                # remove m2m relationship if not in majors from form
                if current_major not in form_majors:
                    me.major.remove(current_major)
            # iterate over the majors in the form
            for form_major in form_majors:
                # add new m2m relationship to student
                if form_major not in me.major.all():
                    me.major.add(form_major)
        except:
            # don't change majors
            pass

        # replicate the same thing for the other m2m field
        try:
            form_blocked_pks = set(form.data.getlist('blocked_kids'))
            current_blocked = me.blocked_kids.all()
            # most people will not being blocking other students
            if form_blocked_pks or current_blocked:
                form_blocked = [Student.objects.get(pk=pk) for pk in form_blocked_pks]
                for current_block in current_blocked:
                    if current_block not in form_blocked:
                        me.blocked_kids.remove(current_block)
                for form_block in form_blocked:
                    if form_block not in current_blocked:
                        me.blocked_kids.add(form_block)
        except:
            pass

        me.user.first_name = no_nums(form.data['first_name'])
        me.user.last_name = no_nums(form.data['last_name'])
        me.gender = form.data.getlist('gender')
        me.show_gender = strtobool(form.data.get('show_gender', 'False'))
        me.graduating_year = form.data['graduating_year']
        me.user.save()
        me.save()

        return super(UpdateStudent, self).form_valid(form)

    def get_success_url(self):

        if self.request.user.student.recent_changes() == 2:

            msg = """To safeguard everyone\'s privacy, you have just one remaining room
                     change for the semester before you\'ll need to send us an email at
                     roomlist@lists.srct.gmu.edu."""
            messages.add_message(self.request, messages.WARNING, msg)

        return reverse('detail_student',
                       kwargs={'slug': self.request.user.username})


class DeleteStudent(LoginRequiredMixin, StudentContextMixin, FormView):
    form_class = FarewellFeedbackForm
    template_name = 'delete_student.html'

    def get(self, request, *args, **kwargs):

        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]
        try:
            student = Student.objects.get(user__username=url_uname)
        except ObjectDoesNotExist:
            raise Http404

        if student.is_staff():
            staff_msg = """To delete your account, contact us if you are no longer a
                           Resident Advisor or Director at
                           <a href="mailto:roomlist@lists.srct.gmu.edu">
                           roomlist@lists.srct.gmu.edu</a>."""
            messages.add_message(self.request, messages.ERROR, mark_safe(staff_msg))
            return HttpResponseRedirect(reverse('update_student',
                                                kwargs={'slug': self.request.user.username}))
        elif not(url_uname == self.request.user.username):
            return HttpResponseRedirect(reverse('delete_student',
                                                kwargs={'slug': self.request.user.username}))
        else:
            return super(DeleteStudent, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        student = self.request.user.student

        # we're using this api because opening smtp connections is taxing in
        # that it takes time-- we want to send both emails at once without
        # having to log in and out and back in and out again
        connection = get_connection()

        # send email to the student
        text_path = 'email/farewell.txt'
        html_path = 'email/farewell.html'

        if form.cleaned_data['leaving']:
            context = {
                'student_name': student.get_first_name_or_uname,
                'special_message': "We're glad you gave our service a try."
            }
        else:
            context = {
                'student_name': student.get_first_name_or_uname,
                'special_message': "We wish you luck in your time after Mason!"
            }

        subject = "You successfully deleted your account on Roomlist"
        to = user.email

        student_email = create_email(text_path, html_path, subject, to, context)

        # send feedback to the admins if there is feedback to send
        if form.cleaned_data['feedback']:
            text_path = 'email/feedback.txt'
            html_path = 'email/feedback.html'

            date_text = student.created.strftime('%A, %B %d, %Y')

            if form.cleaned_data['leaving']:
                leaving = ""
            else:
                leaving = "not"

            context = {
                'student_name':  student.get_first_name_or_uname,
                'signup_date': date_text,
                'leaving': leaving,
                'feedback': form.cleaned_data['feedback']
            }

            subject = "Feedback from Roomlist account deletion"
            to = 'roomlist@lists.srct.gmu.edu'

            feedback_email = create_email(text_path, html_path, subject, to, context)

            connection.send_messages([student_email, feedback_email])
        else:
            connection.send_messages([student_email])

        # yes, we do have to manually close the connection
        connection.close()

        # delete both the student object and the student object
        confirmations = Confirmation.objects.filter(confirmer=student)
        if confirmations:
            for confirmation in confirmations:
                confirmation.delete()
        student.delete()
        user.delete()

        return super(DeleteStudent, self).form_valid(form)

    def get_success_url(self):
        return reverse('homepage')


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
        me = self.request.user.student

        # all students in the major-- needs to be ordered for groupby
        major_students = Student.objects.filter(major__in=[self.get_object()]).order_by('graduating_year')

        students_by_year = OrderedDict()  # we're ordering from senior on down

        for year, students in groupby(major_students, lambda student: student.graduating_year):
            student_list = list(students)  # students without the casting is an iterator
            visible_students = shadowbanning(me, student_list)  # remove blocked students
            students_by_year[year] = visible_students  # remembers insertion order

        context['students_by_year'] = students_by_year

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
        # [u'', u'accounts', u'student', u'gmason', u'flag', u'confirmer']
        confirmer_uname = current_url.split('/')[3]
        student_uname = current_url.split('/')[5]
        try:
            confirmer = Student.objects.get(user__username=confirmer_uname)
            student = Student.objects.get(user__username=student_uname)
            flags = Confirmation.objects.filter(confirmer=confirmer,
                                                student=student).count()
        except ObjectDoesNotExist:
            raise Http404

        # you can't flag yourself
        if confirmer == student:
            raise Http404

        # check that the confirmer is on the floor of the student
        if not on_the_same_floor(student, confirmer):
            return HttpResponseForbidden()

        # check if the confirmer has already flagged the student
        if flags >= 1:
            return HttpResponseForbidden()

        # you can't see the page if the person has banned you
        if confirmer in student.blocked_kids.all():
            raise Http404

        return super(CreateConfirmation, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateConfirmation, self).get_context_data(**kwargs)

        # duplicated code
        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[5]

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
        url_uname = current_url.split('/')[5]

        confirmer = Student.objects.get(user=self.request.user)
        student = Student.objects.get(slug=url_uname)

        form.instance.confirmer = confirmer
        form.instance.student = student

        return super(CreateConfirmation, self).form_valid(form)

    def get_success_url(self):
        # redirect to the flagged student page when saving
        return reverse('detail_student',
                       kwargs={'slug': self.object.student.slug})


class DeleteConfirmation(LoginRequiredMixin, DeleteView):
    model = Confirmation
    template_name = 'delete_confirmation.html'

    login_url = 'login'

    def get(self, request, *args, **kwargs):
        requester = self.request.user.student

        current_url = self.request.get_full_path()
        confirmer_uname = current_url.split('/')[3]
        # not catching exceptions here; that's handled in get_object
        confirmer = Student.objects.get(user__username=confirmer_uname)

        # only the person who created the confirmation may delete it
        if not(requester == confirmer):
            return HttpResponseForbidden()
        # however, if the confirmation just flat out doesn't exist...
        else:
            try:
                confirmer = self.get_object().confirmer
            except ObjectDoesNotExist:
                raise Http404
            else:
                return super(DeleteConfirmation, self).get(request, *args, **kwargs)

    def get_object(self):
        current_url = self.request.get_full_path()
        # [u'', u'accounts', u'student', u'gmason', u'flag', u'confirmer', delete]
        confirmer_uname = current_url.split('/')[3]
        student_uname = current_url.split('/')[5]

        try:
            confirmer = Student.objects.get(user__username=confirmer_uname)
            student = Student.objects.get(user__username=student_uname)
            confirmation = Confirmation.objects.get(confirmer=confirmer, student=student)
        except ObjectDoesNotExist:
            raise Http404
        return confirmation

    def get_success_url(self):
        return reverse('detail_student',
                       kwargs={'slug': self.object.student.slug})
