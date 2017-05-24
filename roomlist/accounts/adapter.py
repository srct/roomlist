# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.forms import Form
# third party imports
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import social_account_removed
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


class RemoveSocialConfirmationView(LoginRequiredMixin, FormView):
    """To customize where users are sent when removing their social media connections.
    We have written our own template to handle this feature that is much prettier than
    the one provided by allauth."""

    # we're not using this, but we're not allowed to have None
    form_class = Form

    template_name = "social/remove_social.html"
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        current_url = self.request.get_full_path()
        # [u'', u'accounts', u'student', u'dbond2', u'settings', u'social', u'github', u'remove', u'']
        social_application = current_url.split('/')[6]

        connected_accounts = [account.provider
                              for account in request.user.socialaccount_set.all()]

        # first, check that the user has an account of the type specified in the url
        if not(social_application in connected_accounts):
            # no social media accounts? back to the settings page with you!
            messages.add_message(self.request,
                                 messages.INFO,
                                 "Select a social media icon to connect an account.")
            return HttpResponseRedirect(reverse('update_student',
                                        kwargs={'slug': self.request.user.username}))
        else:
            return super(RemoveSocialConfirmationView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RemoveSocialConfirmationView, self).get_context_data(**kwargs)

        current_url = self.request.get_full_path()
        social_application = current_url.split('/')[6]

        for account in self.request.user.socialaccount_set.all():
            if account.provider == social_application:
                branding = account.get_provider().name

        context['branding'] = branding
        context['application'] = social_application
        return context

    def post(self, request, *args, **kwargs):
        current_url = self.request.get_full_path()
        social_application = current_url.split('/')[6]

        for account in request.user.socialaccount_set.all():
            if account.provider == social_application:
                social_account = account
                branding = account.get_provider().name

        # we do not need to use validate_disconnect, because accounts are not
        # associated with being able to log in
        try:
            social_account.delete()
            social_account_removed.send(sender=SocialAccount,
                                        request=request,
                                        socialaccount=social_account)
            message = "%s has been successfully disconnected." % branding 
            messages.add_message(self.request,
                                 messages.SUCCESS,
                                 message)
        # if multiple posts went in, there won't be any 'social_account' or 'branding'
        # basically, that means it's already gone and it already works
        except UnboundLocalError:
            get_account_adapter().add_message(self.request,
                                              messages.SUCCESS,
                                              'socialaccount/messages/'
                                              'account_disconnected.txt')

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('update_student',
                        kwargs={'slug': self.request.user.username})
