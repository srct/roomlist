# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django import forms
# third party imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import PrependedText, AppendedText
from multiselectfield import MultiSelectFormField
# imports from your apps
from .models import Student, Room, Major
from housing.models import Building


class StudentUpdateForm(forms.Form):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    gender = MultiSelectFormField(choices=Student.GENDER_CHOICES,
                                  label='Gender Identity (please choose all that apply)')

    #neighborhood = forms.ChoiceField(choices=Building.NEIGHBOURHOOD_CHOICES)
    #building = forms.ModelChoiceField(queryset=Building.objects.filter(neighbourhood=neighborhood)
    #floor = forms.ModelChoiceField(queryset=Floor.objects.filter(building=building)
    #room = forms.ModelChoiceField(queryset=Room.objects.filter(floor=floor))

    privacy = forms.ChoiceField(choices=Student.PRIVACY_CHOICES)
    major = forms.ModelChoiceField(queryset=Major.objects.all())
    graduating_year = forms.IntegerField(label='Graduating Year')


class WelcomeNameForm(forms.Form):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    gender = MultiSelectFormField(choices=Student.GENDER_CHOICES, label='Gender Identity (please choose all that apply)')


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
