# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django import forms
from django.core.exceptions import ValidationError
# third party imports
from multiselectfield import MultiSelectFormField
# imports from your apps
from accounts.models import Student
from accounts.forms import SelectRoomField, BooleanRadioField
from housing.models import Room


class WelcomeNameForm(forms.Form):

    first_name = forms.CharField(required=False, max_length=30)
    first_name.widget.attrs['class'] = 'form-control'
    last_name = forms.CharField(required=False, max_length=30)
    last_name.widget.attrs['class'] = 'form-control'
    gender = MultiSelectFormField(choices=Student.GENDER_CHOICES, required=False)
    show_gender = BooleanRadioField()


class WelcomePrivacyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WelcomePrivacyForm, self).__init__(*args, **kwargs)
        self.fields['privacy'].widget.attrs['class'] = 'form-control'
        if self.instance.recent_changes() > 2:
            self.fields['room'].widget = forms.widgets.HiddenInput()
        else:
            self.fields['room'] = SelectRoomField(queryset=Room.objects.all(), required=False)

    on_campus = BooleanRadioField()

    def clean(self):
        cleaned_data = super(WelcomePrivacyForm, self).clean()
        form_room = cleaned_data.get('room')
        if not(form_room is None):
            students_in_room = Student.objects.filter(room=form_room).count()
            # print(students_in_room)
            # like in bookshare, I have no idea why the form errors don't display.
            if students_in_room > 12:
                raise ValidationError(_('Too many students in room (%d).' % students_in_room), code='invalid')

    class Meta:
        model = Student
        fields = ('room', 'privacy', 'on_campus')


class WelcomeMajorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WelcomeMajorForm, self).__init__(*args, **kwargs)
        self.fields['graduating_year'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Student
        fields = ('major', 'graduating_year', )


class WelcomeSocialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WelcomeSocialForm, self).__init__(*args, **kwargs)
        self.fields['completedSocial'].widget = forms.widgets.HiddenInput()

    class Meta:
        model = Student
        fields = ('completedSocial', )
