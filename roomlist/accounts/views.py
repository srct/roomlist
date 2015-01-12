from django.shortcuts import render, get_object_or_404

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from accounts.models import Student
from accounts.forms import StudentForm

from braces.views import LoginRequiredMixin

# create a student
class CreateStudent(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    success_url = '/' #redirect location tba
    login_url = '/'

# details about the student
class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    login_url = '/accounts/login/'

# changeable student settings
class DetailStudentSettings(LoginRequiredMixin, DetailView):
    model = Student
    login_url = '/accounts/login/'


class DetailCurrentStudent(LoginRequiredMixin, DetailView):

    #model = Student

    def get_object(self):
        return get_object_or_404(Student, pk=self.request.session['_auth_user_id'])

class DetailCurrentStudentSettings(LoginRequiredMixin, DetailView):

    #model = Student

    def get_object(self):
        return get_object_or_404(Student, pk=self.request.session['_auth_user_id'])
