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


class StudentUpdateForm(forms.Form):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    gender = MultiSelectFormField(choices=Student.GENDER_CHOICES,
                                  label='Gender Identity (please choose all that apply)')
    room = forms.ModelChoiceField(queryset=Room.objects.all())
    privacy = forms.ChoiceField(choices=Student.PRIVACY_CHOICES)
    major = forms.ModelChoiceField(queryset=Major.objects.all())
    graduating_year = forms.IntegerField(label='Graduating Year')


class WelcomeNameForm(forms.Form):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    gender = MultiSelectFormField(choices=Student.GENDER_CHOICES, label='Gender Identity (please choose all that apply)')


class WelcomePrivacyForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['room', 'privacy', ]


class WelcomeSocialForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['completedSocial', ]
