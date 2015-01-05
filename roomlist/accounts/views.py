from django.shortcuts import render

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
    login_url = '/'
