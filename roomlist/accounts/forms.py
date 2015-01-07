from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from crispy_forms.bootstrap import PrependedText, AppendedText, FormActions

from accounts.models import Student

# form to create student
class StudentForm( forms.ModelForm ):

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

