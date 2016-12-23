# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# third party imports
from multiselectfield import MultiSelectFormField
from haystack.forms import SearchForm
# imports from your apps
from .models import Student, Major
from housing.models import Building, Floor, Room


class SelectRoomWidget(forms.widgets.Select):
    """A series of dropdowns in which a student can filter through housing options."""

    template_name = 'room_select_widget.html'

    def __init__(self, user=None, attrs=None, rooms=None, floors=None, buildings=None, neighborhoods=None):
        super(SelectRoomWidget, self).__init__(attrs)
        # attrs to be implemented later (allows specifying css class, for example)
        if attrs:
            print("Sorry about that, but we're currently ignoring your fancy attrs.")
        # should probably type check the other fields too
        if rooms is None:
            self.rooms = Room.objects.all().prefetch_related('floor')
        else:
            if not all(isinstance(thing, Room) for thing in rooms):
                raise TypeError("Rooms in a SelectRoomWidget must all be Rooms!")
        if floors is None:
            self.floors = Floor.objects.all().prefetch_related('building')
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
    """A special field for room selection, using the room selection widget."""
    widget = SelectRoomWidget

#    should raise error if user hasn't actually selected room, made it to end of selectors
#    def clean(self, value):


class BooleanRadioField(forms.TypedChoiceField):
    """Displays booleans as a radio selector, rather than checkboxes."""

    def __init__(self, *args, **kwargs):
        boolean_choices = ((True, 'Yes'), (False, 'No'))

        kwargs['widget'] = forms.RadioSelect
        kwargs['choices'] = boolean_choices
        kwargs['coerce'] = bool
        kwargs['required'] = True
        super(BooleanRadioField, self).__init__(*args, **kwargs)


class StudentUpdateForm(forms.Form):

    first_name = forms.CharField(required=False, max_length=30)
    first_name.widget.attrs['class'] = 'form-control'
    last_name = forms.CharField(required=False, max_length=30)
    last_name.widget.attrs['class'] = 'form-control'
    gender = MultiSelectFormField(choices=Student.GENDER_CHOICES,
                                  required=False)
    show_gender = BooleanRadioField(required=True)

    on_campus = BooleanRadioField(required=True)
    room = SelectRoomField(queryset=Room.objects.all(), required=False)

    privacy = forms.TypedChoiceField(choices=Student.PRIVACY_CHOICES)
    privacy.widget.attrs['class'] = 'form-control'
    # exclude self from request in form instantiation
    blocked_kids = forms.ModelMultipleChoiceField(queryset=Student.objects.all(),
                                                  required=False)

    major = forms.ModelMultipleChoiceField(queryset=Major.objects.all(), required=False)
    graduating_year = forms.IntegerField(max_value=9999, min_value=-9999, required=False)
    graduating_year.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(StudentUpdateForm, self).clean()
        form_room = cleaned_data.get('room')
        if not(form_room is None):
            students_in_room = Student.objects.filter(room=form_room).count()
            # print(students_in_room)
            # like in bookshare, I have no idea why the form errors don't display.
            if students_in_room > 12:
                raise ValidationError(_('Too many students in room (%d).' % students_in_room), code='invalid')

    def is_valid(self):
        # errors are not printed in form.as_p?
        # print("In is_valid.")
        # print(self.is_bound, 'is bound')
        # print(self.errors, type(self.errors), 'errors')
        valid = super(StudentUpdateForm, self).is_valid()
        # print(valid)
        return valid


class FarewellFeedbackForm(forms.Form):

    # required = True by default
    leaving = BooleanRadioField(label="Are you graduating or leaving Mason?")
    feedback = forms.CharField(label="Thoughts",
                               max_length=1000,
                               widget=forms.Textarea(attrs={'class': 'form-control'}),
                               required=False)


# we are overwriting the search form to include boostrap css classes
class AccountSearchForm(SearchForm):

    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'type': 'search',
                                                      'class': 'form-control',
                                                      'autofocus': 'autofocus'}))
