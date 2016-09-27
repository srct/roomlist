# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
# third party imports
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.views import ConnectionsView
from allauth.exceptions import ImmediateHttpResponse
from braces.views import LoginRequiredMixin


class AccountAdapter(DefaultSocialAccountAdapter):
    """A custom implementation of a portion of the allauth social media package.

    We're overriding a number of aspects of the allauth account adapter to support
    our special use of the package. We are using CAS, not Django's built-in
    authentication. Accordingly we change the where directed when successfully
    connecting an account and how errors are dealt with. Additionally, we are not using
    the social media accounts to verify or overwrite any aspect of the User model.
    """

    # the request processed by the adapter is one from the successful oauth callback
    # uncomment this method to print what URL you are arriving from
    # def pre_social_login(self, request, sociallogin):
    #     print(request.get_full_path(), 'pre_login')

    def populate_user(self, request, sociallogin, data):
        # This is a hook to populate User attributes, but we expressly don't actually
        # want to overwrite anything from the social media account user. It's intended
        # in the package for when you are using social media for login.
        user = sociallogin.user
        return user

    def get_connect_redirect_url(self, request, socialaccount):
        # where the user is sent if the social account is indeed authenticated
        assert request.user.is_authenticated()

        # we are approximating that if a user has not completed the welcome walkthough,
        # it is likely the page on which they started-- see the pre_social_login method
        if not request.user.student.completedSocial:
            return reverse('welcomeSocial', kwargs={
                'slug': request.user.username,
            })
        else:
            return reverse('update_student', kwargs={
                'slug': request.user.username,
            })

    def authentication_error(self, request, provider_id, error=None, exception=None,
                             extra_context=None):
        """Adds a custom message to the message queue if social media auth fails."""

        error_message = """Looks like something went awry with your social
                           authentication. Wait a moment and try your username and
                           password again. If things are still broken, let us know by
                           sending an email to roomlist@lists.srct.gmu.edu."""

        if not request.user.student.completedSocial:
            # as a reminder, here is how django handles messages
            # https://docs.djangoproject.com/en/1.8/ref/contrib/messages/
            messages.add_message(request, messages.ERROR, error_message)
            social_redirect = HttpResponseRedirect(reverse('welcomeSocial', kwargs={
                                  'slug': request.user.username,
                              }))
            raise ImmediateHttpResponse(social_redirect)
        else:
            messages.add_message(request, messages.ERROR, error_message)
            update_redirect =  HttpResponseRedirect(reverse('update_student', kwargs={
                                  'slug': request.user.username,
                               }))
            raise ImmediateHttpResponse(update_redirect)


class RemoveSocialConfirmationView(LoginRequiredMixin, ConnectionsView):
    """To customize where users are sent when removing their social media connections.
    We have written our own template to handle this feature that is much prettier than
    the one provided by allauth."""

    template_name = "remove_social.html"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if not request.user.socialaccount_set.all():
            # no social media accounts? back to the settings page with you!
            return HttpResponseRedirect(reverse('update_student',
                                        kwargs={'slug': self.request.user.username}))
        else:
            return super(RemoveSocialConfirmationView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        return super(RemoveSocialConfirmationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('update_student',
                        kwargs={'slug': self.request.user.username})
