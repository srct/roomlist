# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.shortcuts import render
from django.views.generic import (View, DetailView, TemplateView)
# third party imports
from braces.views import LoginRequiredMixin
from accounts.models import Student
# imports from your apps
from housing.views import shadowbanning


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
        roomies = Student.objects.filter(room=me.room).exclude(user__username=me)
        floories = Student.objects.filter(room__floor=me.get_floor()).exclude(user__username=me).exclude(room=me.room).order_by('room')

        my_majors = tuple(me.major.all())
        students_by_major = {}
        for major in my_majors:
            students_by_major[major] = Student.objects.filter(major__in=[major]).exclude(user__username=me).order_by('?')[:8]
        majormates = students_by_major

        context["roomies"] = shadowbanning(me, roomies)
        context["floories"] = shadowbanning(me, floories)
        context["majormates"] = shadowbanning(me, majormates)
        return context


class LandingPageNoAuth(DetailView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
