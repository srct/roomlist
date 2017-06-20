# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.contrib import messages
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View, DetailView, TemplateView, RedirectView
from django.utils.safestring import mark_safe
# third party imports
from braces.views import LoginRequiredMixin
# imports from your apps
from accounts.models import Student, Major
from core.utils import shadowbanning


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            view = LandingPage.as_view()
            return view(request, *args, **kwargs)
        else:
            view = LandingPageNoAuth.as_view()
            return view(request, *args, **kwargs)


class LandingPage(LoginRequiredMixin, TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super(LandingPage, self).get_context_data(**kwargs)
        me = Student.objects.get(user=self.request.user)
        context['me'] = me

        # Create Dictionaries to store Students that meet criteria
        roomies = Student.objects.filter(room=me.room).exclude(user=me.user)
        floories = Student.objects.filter(room__floor=me.get_floor()).exclude(user=me.user).exclude(room=me.room).order_by('room')

        my_majors = tuple(me.major.all())
        students_by_major = {}
        for major in my_majors:
            major_students = Student.objects.filter(major__in=[major]).exclude(user=me.user).order_by('?')[:8]
            censored_major = shadowbanning(me, major_students)
            students_by_major[major] = censored_major

        context["roomies"] = shadowbanning(me, roomies)
        context["floories"] = shadowbanning(me, floories)
        context["majormates"] = students_by_major
        return context


class LandingPageNoAuth(DetailView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# redirecting urls
class RedirectSettings(RedirectView):

    permanent = True

    # we're not including loginrequired, because that's already part of where we're
    # sending the student to-- this is just about changing the url
    def get_redirect_url(self, *args, **kwargs):
        slug = self.request.user.username
        return reverse('update_student',
                       kwargs={'slug': slug})


class RedirectSlug(RedirectView):

    permanent = True

    # we're not including loginrequired, because that's already part of where we're
    # sending the student to-- this is just about changing the url
    def get_redirect_url(self, *args, **kwargs):
        current_url = self.request.get_full_path()
        # print(self.request)
        # [u'', u'gmason']
        slug = current_url.split('/')[1]
        # print(slug)

        try:
            # print('trying student')
            student = Student.objects.get(user__username=slug)
            return reverse('detail_student',
                           kwargs={'slug': slug})
        except ObjectDoesNotExist:
            # print('trying major')
            try:
                major = Major.objects.get(slug=slug)
                return reverse('detail_major',
                               kwargs={'slug': slug})
            except ObjectDoesNotExist:
                raise Http404
        else:
            return Http404


class BlockingMiddleware(object):
    """Prevent students who have been blocked from accessing any
       login-protected content.

       This is implemented as middleware to immediately force a user's logout,
       not just to block them once they've logged out and are logging back in."""

    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.user.is_authenticated():
            if request.user.student.blocked:
                msg = """You are not permitted to use Roomlist. Please contact us at
                         <a href="mailto:roomlist@lists.srct.gmu.edu">
                         roomlist@lists.srct.gmu.edu</a>
                         if you believe this to be an error."""
                messages.add_message(request, messages.ERROR, mark_safe(msg))

                logout(request)
