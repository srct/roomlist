# standard library imports
from __future__ import absolute_import, print_function
from distutils.util import strtobool
# core django imports
from django.shortcuts import redirect
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
# third party imports
from braces.views import LoginRequiredMixin
from ratelimit.decorators import ratelimit
# imports from your apps
from accounts.models import Student, Confirmation
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

        me.user.first_name = form.data['first_name']
        me.user.last_name = form.data['last_name']

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
        form.fields['major'].widget.attrs['class'] = 'chosen-select'

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

        form = WelcomeMajorForm(initial={'major': me.major,
                                         'graduating_year': me.graduating_year, })

        context['my_form'] = form

        context['student'] = me

        return context

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='10/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(WelcomeMajor, self).post(request, *args, **kwargs)

    def form_valid(self, form):

        me = Student.objects.get(user=self.request.user)

        me.major = form.instance.major
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

        return super(WelcomeSocial, self).form_valid(form)

    def get_success_url(self):

        if self.request.user.student.totally_done():
            messages.add_message(self.request, messages.SUCCESS,
                                 "You successfully finished the welcome walkthrough!")

        return reverse('detail_student',
                       kwargs={'slug': self.request.user.username})
