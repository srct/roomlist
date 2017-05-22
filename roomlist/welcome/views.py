# standard library imports
from __future__ import absolute_import, print_function
from distutils.util import strtobool
from datetime import date
# core django imports
from django.shortcuts import redirect
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
# third party imports
from braces.views import LoginRequiredMixin
from ratelimit.decorators import ratelimit
# imports from your apps
from accounts.models import Student, Confirmation, Major
from core.utils import create_email, no_nums, get_semester
from housing.models import Room
from .forms import (WelcomeNameForm, WelcomeMajorForm,
                    WelcomePrivacyForm, WelcomeSocialForm)


settings_redirect = """You've already finished the welcome walkthrough.
                       Your user settings can now be changed here on this page."""


class WelcomeName(LoginRequiredMixin, FormView):
    """Student adds first and last name, and gender and gender display."""

    template_name = 'welcome_name.html'
    form_class = WelcomeNameForm
    login_url = 'login'

    # students are redirected to the normal settings page once they have completed
    # the welcome walkthrough in its entirety
    def get(self, request, *args, **kwargs):

        if self.request.user.student.totally_done():
            messages.add_message(request, messages.INFO, settings_redirect)
            return redirect(reverse('update_student',
                            kwargs={'slug': self.request.user.username}))
        else:
            return super(WelcomeName, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WelcomeName, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)

        form = WelcomeNameForm(initial={'first_name': me.user.first_name,
                                        'last_name': me.user.last_name,
                                        'gender': me.gender,
                                        'show_gender': me.show_gender, })

        form.fields['first_name'].widget.attrs['class'] = 'form-control'
        form.fields['last_name'].widget.attrs['class'] = 'form-control'

        context['my_form'] = form
        return context

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='10/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(WelcomeName, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        me.user.first_name = no_nums(form.data['first_name'])
        me.user.last_name = no_nums(form.data['last_name'])

        me.gender = form.data.getlist('gender')
        me.show_gender = strtobool(form.data.get('show_gender', 'False'))

        me.completedName = True

        me.user.save()
        me.save()

        return super(WelcomeName, self).form_valid(form)

    def get_success_url(self):
        return reverse('welcomePrivacy')


class WelcomePrivacy(LoginRequiredMixin, FormView):
    """Student adds off-or-on campus status, and if on-campus, housing and privacy."""

    form_class = WelcomePrivacyForm
    template_name = 'welcome_privacy.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):

        if self.request.user.student.totally_done():
            messages.add_message(request, messages.INFO, settings_redirect)
            return redirect(reverse('update_student',
                            kwargs={'slug': self.request.user.username}))
        else:
            return super(WelcomePrivacy, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WelcomePrivacy, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)

        form = WelcomePrivacyForm(initial={'on_campus': me.on_campus,
                                           'privacy': me.privacy, })

        form.fields['room'].widget.user = self.request.user

        context['my_form'] = form

        context['student'] = me

        return context

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='10/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(WelcomePrivacy, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

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

        if current_room != form_room:
            form.instance.times_changed_room += 1
            Confirmation.objects.filter(student=me).delete()

        me.on_campus = on_campus
        me.room = form_room

        me.completedPrivacy = True

        me.save()

        return super(WelcomePrivacy, self).form_valid(form)

    def get_success_url(self):
        return reverse('welcomeMajor')


class WelcomeMajor(LoginRequiredMixin, FormView):
    """Student adds major and graduation year."""

    template_name = 'welcome_major.html'
    form_class = WelcomeMajorForm
    login_url = 'login'

    def get(self, request, *args, **kwargs):

        if self.request.user.student.totally_done():
            messages.add_message(request, messages.INFO, settings_redirect)
            return redirect(reverse('update_student',
                            kwargs={'slug': self.request.user.username}))
        else:
            return super(WelcomeMajor, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WelcomeMajor, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)

        form = WelcomeMajorForm(initial={'major': me.major.all(),
                                         'graduating_year': me.graduating_year, })

        form.fields['major'].widget.attrs['class'] = 'chosen-select'

        context['my_form'] = form
        context['student'] = me

        return context

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='10/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(WelcomeMajor, self).post(request, *args, **kwargs)

    def form_valid(self, form):

        me = Student.objects.get(user=self.request.user)

        try:
            # see UpdateStudent in accounts/ for a detailed explanation
            # but m2m fields are more difficult to manage than other relationships
            form_major_pks = set(form.data.getlist('major')[:2])
            form_majors = [Major.objects.get(pk=pk) for pk in form_major_pks]
            # a student likely won't have any majors on the welcome walkthrough
            # using Python's implicit evaluation (empty is False, anything is True)
            if me.major.all():
                for current_major in me.major.all():
                    if current_major not in form_majors:
                        me.major.remove(current_major)
            for form_major in form_majors:
                if form_major not in me.major.all():
                    me.major.add(form_major)
        except:
            pass

        me.graduating_year = form.instance.graduating_year

        me.completedMajor = True

        me.save()

        return super(WelcomeMajor, self).form_valid(form)

    def get_success_url(self):
        return reverse('welcomeSocial')


class WelcomeSocial(LoginRequiredMixin, FormView):
    """Student connects social media accounts. Redirects to settings page when done."""

    form_class = WelcomeSocialForm
    template_name = 'welcome_social.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):

        if self.request.user.student.totally_done():
            messages.add_message(request, messages.INFO, settings_redirect)
            return redirect(reverse('update_student',
                            kwargs={'slug': self.request.user.username}))
        else:
            return super(WelcomeSocial, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WelcomeSocial, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)

        context['student'] = me

        return context

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='10/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(WelcomeSocial, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        me.completedSocial = True

        me.save()

        # send students a welcome email
        text_path = 'email/welcome.txt'
        html_path = 'email/welcome.html'

        today = date.today()
        semester = "%s %s" % (get_semester(today), today.strftime('%Y'))

        context = {
            'student_name': me.get_first_name_or_uname,
            'semester': semester
        }

        subject = "Welcome to Roomlist, %s" % me.get_first_name_or_uname()
        to = me.user.email

        welcome_email = create_email(text_path, html_path, subject, to, context)

        welcome_email.send()

        return super(WelcomeSocial, self).form_valid(form)

    def get_success_url(self):

        if self.request.user.student.totally_done():
            messages.add_message(self.request, messages.SUCCESS,
                                 "You successfully finished the welcome walkthrough!")

        return reverse('detail_student',
                       kwargs={'slug': self.request.user.username})
