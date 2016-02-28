# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.shortcuts import render
from django.views.generic import (View, DetailView, TemplateView)
# third party imports
from braces.views import LoginRequiredMixin
from cas.views import login as cas_login
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
        majormates = Student.objects.filter(major=me.major).exclude(user__username=me).order_by('?')[:8]

        context["roomies"] = shadowbanning(me, roomies)
        context["floories"] = shadowbanning(me, floories)
        context["majormates"] = shadowbanning(me, majormates)
        # Hack to Correctly Display Building plus Floor
        #floor = str(me.get_floor())
        #if floor[len(floor)-1:len(floor)] == "1":
        #    context["home"] = "%s %s" %(me.get_building(), 'First')
        #elif floor[len(floor)-1:len(floor)] == "2":
        #    context["home"] = "%s %s" %(me.get_building(), 'Second')
        #else:
        #    context["home"] = "%s %s" %(me.get_building(), 'Third')

        return context

class LandingPageNoAuth(DetailView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
