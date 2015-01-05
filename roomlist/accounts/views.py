from django.shortcuts import render

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from accounts.models import Student

from braces.views import LoginRequiredMixin

# details about the student
class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    login_url = '/'
