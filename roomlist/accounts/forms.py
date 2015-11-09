# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
# third party imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import PrependedText, AppendedText
from multiselectfield import MultiSelectFormField
# imports from your apps
from .models import Student, Major
from housing.models import Building, Floor, Room


class SelectRoomWidget(forms.widgets.Select):

    template_name = 'room_select_widget.html'

    def __init__(self, rooms=Room.objects.all(), floors=Floor.objects.all(),
                 buildings=Building.objects.all(), neighborhoods=Building.NEIGHBOURHOOD_CHOICES):
        # should probably type check the other fields too
        if not all(isinstance(thing, Room) for thing in rooms):
            raise TypeError("Rooms in a SelectRoomWidget must all be Rooms!")

    def render(self, rooms, floors, buildings, neighborhoods):
        context = {
            'neighborhoods': neighborhoods,
            'buildings': buildings,
            'floors': floors,
            'rooms': rooms,
        }
        return mark_safe(render_to_string(self.template_name, context))


class StudentUpdateForm(forms.Form):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    gender = MultiSelectFormField(choices=Student.GENDER_CHOICES,
                                  label='Gender Identity (please choose all that apply)')

    room = forms.ModelChoiceField(widget=SelectRoomWidget())

    privacy = forms.ChoiceField(choices=Student.PRIVACY_CHOICES)
    major = forms.ModelChoiceField(queryset=Major.objects.all())
    graduating_year = forms.IntegerField(label='Graduating Year')


class WelcomeNameForm(forms.Form):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    gender = MultiSelectFormField(choices=Student.GENDER_CHOICES,
                                  label='Gender Identity (please choose all that apply)')


class WelcomePrivacyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WelcomePrivacyForm, self).__init__(*args, **kwargs)
        if self.instance.recent_changes() >= 2:
            self.fields['room'].widget = forms.widgets.HiddenInput()

    class Meta:
        model = Student
        fields = ('room', 'privacy', )


class WelcomeSocialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WelcomeSocialForm, self).__init__(*args, **kwargs)
        self.fields['completedSocial'].widget = forms.widgets.HiddenInput()

    class Meta:
        model = Student
        fields = ('completedSocial', )
