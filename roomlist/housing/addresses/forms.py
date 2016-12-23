# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from localflavor.us.us_states import US_STATES as states


class AddressWidget(forms.widgets.Widget):

    template_name = 'address_widget.html'

    def __init__(self, user=None, attrs=None):
        super(AddressWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        # I'm sure I should be elated about i18n, but not feeling that way at the moment
        actual_strings = [(abbr, unicode(state_name)) for abbr, state_name in states]
        context = {
            'states': actual_strings,
        }
        return mark_safe(render_to_string(self.template_name, context))


class AddressField(forms.CharField):

    widget = AddressWidget
