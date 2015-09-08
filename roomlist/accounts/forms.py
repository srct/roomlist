# core django imports
from django import forms
# third party imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import PrependedText, AppendedText
from multiselectfield import MultiSelectFormField
# imports from your apps
from .models import Student


# form to create student
class StudentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'user',
            PrependedText('room', 'Room'),
            'class',
            AppendedText('major', 'Major'),
        )
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        super(StudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Student


class UserSettingsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'user',
            PrependedText('room', 'Room'),
            'class',
            AppendedText('major', 'Major'),
        )
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        super(StudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Student

class WelcomeNameForm(forms.Form):

    first_name = forms.CharField(label='First Name')

    last_name = forms.CharField(label='Last Name')

    gender = MultiSelectFormField(choices=Student.GENDER_CHOICES, label='Gender Identity (please choose all that apply)')
