# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.core.exceptions import ValidationError
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

    def __init__(self, user=None, attrs=None, rooms=None, floors=None, buildings=None, neighborhoods=None):
        super(SelectRoomWidget, self).__init__(attrs)
        # attrs to be implemented later (allows specifying css class, for example)
        if attrs:
            print("Sorry about that, but we're currently ignoring your fancy attrs.")
        # should probably type check the other fields too
        if rooms is None:
            self.rooms = Room.objects.all()
        else:
            if not all(isinstance(thing, Room) for thing in rooms):
                raise TypeError("Rooms in a SelectRoomWidget must all be Rooms!")
        if floors is None:
            self.floors = Floor.objects.all()
        if buildings is None:
            self.buildings = Building.objects.all()
        if neighborhoods is None:
            self.neighborhoods = Building.NEIGHBOURHOOD_CHOICES

    def render(self, name, value, attrs=None):
        context = {
            'neighborhoods': self.neighborhoods,
            'buildings': self.buildings,
            'floors': self.floors,
            'rooms': self.rooms,
        }
        if self.user is not None:
            context['user'] = self.user
        return mark_safe(render_to_string(self.template_name, context))


class SelectRoomField(forms.models.ModelChoiceField):
    widget = SelectRoomWidget

#    should raise error if user hasn't actually selected room, made it to end of selectors
#    def clean(self, value):

class StudentUpdateForm(forms.Form):

    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    gender = MultiSelectFormField(choices=Student.GENDER_CHOICES,
                                  label='Gender Identity (please choose all that apply)',
                                  required=False)

    room = SelectRoomField(queryset=Room.objects.all(), label='', required=False)

    privacy = forms.ChoiceField(choices=Student.PRIVACY_CHOICES)
    major = forms.ModelChoiceField(queryset=Major.objects.all(), required=False)
    graduating_year = forms.IntegerField(label='Graduating Year')


    def is_valid(self):
        # errors are not printed in form.as_p?
        #print("In is_valid.")
        #print(self.is_bound, 'is bound')
        #print(self.errors, type(self.errors), 'errors')
        valid = super(StudentUpdateForm, self).is_valid()
        #print(valid)
        return valid

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
        else:
            self.fields['room'] = SelectRoomField(queryset=Room.objects.all(),
                                                  label='', required=False)

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
