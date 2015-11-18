# standard library imports
from __future__ import absolute_import, print_function
from datetime import datetime, timedelta
# core django imports
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.contrib import messages
from django.http import HttpResponseRedirect
# third party imports
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.views import ConnectionsView
from allauth.socialaccount.forms import DisconnectForm
from allauth.exceptions import ImmediateHttpResponse
from braces.views import LoginRequiredMixin

class AccountAdapter(DefaultSocialAccountAdapter):

    # the request processed by the adapter is one from the successful oauth callback

    #def pre_social_login(self, request, sociallogin):
        #print(request.get_full_path(), 'pre_login')

    def populate_user(self, request, sociallogin, data):
        # we don't actually want to overwrite anything from the
        # social media account user
        user = sociallogin.user
        return user

    def get_connect_redirect_url(self, request, socialaccount):
        # where the user is sent if the social account is indeed authenticated
        assert request.user.is_authenticated()
        #print(request.get_full_path())
        #if 'welcome' in request.get_full_path():

        # ergo, we go with more of an approximation (at least for now)

        if not request.user.student.completedSocial:
            return reverse('welcomeSocial', kwargs={
                'slug': request.user.username,
            })
        else:
            return reverse('updateStudent', kwargs={
                'slug': request.user.username,
            })

    def authentication_error(self, request, provider_id, error=None, exception=None,
                             extra_context=None):

        error_message = """Looks like something went awry with your social
                           authentication. Wait a moment and try your username and
                           password again. If things are still broken, let us know by
                           sending an email to roomlist@lists.srct.gmu.edu."""

        if not request.user.student.completedSocial:
            messages.add_message(request, messages.ERROR, error_message)
            social_redirect = HttpResponseRedirect(reverse('welcomeSocial', kwargs={
                                  'slug': request.user.username,
                              }))
            raise ImmediateHttpResponse(social_redirect)
        else:
            messages.add_message(request, messages.ERROR, error_message)
            update_redirect =  HttpResponseRedirect(reverse('updateStudent', kwargs={
                                  'slug': request.user.username,
                              }))
            raise ImmediateHttpResponse(update_redirect)

class RemoveSocialConfirmationView(LoginRequiredMixin, ConnectionsView):
    template_name = "remove_social.html"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if not request.user.socialaccount_set.all():
            # no social media accounts? back to the settings page with you!
            return HttpResponseRedirect(reverse('updateStudent',
                                        kwargs={'slug':self.request.user.username}))
        else:
            return super(RemoveSocialConfirmationView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        return super(RemoveSocialConfirmationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('updateStudent',
                        kwargs={'slug':self.request.user.username})
