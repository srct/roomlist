# core django imports
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, ListView, UpdateView, UpdateView, DeleteView
# third party imports
from braces.views import LoginRequiredMixin
# imports from your apps
from .models import Student


# update a student (students are *created* on first login via CAS)
class UpdateStudent(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ['room', 'privacy',]
    context_object_name = 'student'
    template_name = 'updateStudent.html'

    login_url = 'login'

    def get(self, request, *args, **kwargs):

        current_url = self.request.get_full_path()
        url_uname = current_url.split('/')[3]

        print url_uname, self.request.user.username

        if not(url_uname == self.request.user.username):
            print "I'm sorry, what now?"
            return HttpResponseForbidden()
        else:
            return super(UpdateStudent, self).get(request, *args, **kwargs)

class UpdateStudentMajor(LoginRequiredMixin, UpdateView):
    models = Student
    fields = ['major',]
    template_name = 'updateStudentMajor.html'

    login_url = 'login'

    # copied from below
#    def get_object(self):
#        return get_object_or_404(Student, pk=self.request.session['_auth_user_id'])

# details about the student
class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'detailStudent.html'

    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(DetailStudent, self).get_context_data(**kwargs)

        # requesting_student = Student.objects.get(user=self.request.user)
        requesting_student_filter = Student.objects.filter(user=self.request.user)
        requesting_student = requesting_student_filter[0]

        def onFloor():
            floor_status = False
            if requesting_student.get_floor() == self.get_object().get_floor():
                floor_status = True
            return floor_status

        def inBuilding():
            floor_status = False
            if requesting_student.get_building() == self.get_object().get_building():
                floor_status = True
            return floor_status

        def shares():
            student_shares = False
            # if the student's privacy is floor and the requesting user is on their floor
            if(self.get_object().privacy == 'floor') and onFloor():
                student_shares = True
            # if the student's privacy is building and the requesting users is on their floor or in their building
            elif(self.get_object().privacy == 'building') and inBuilding():
                student_shares = True
            # if the student's privacy is set to 'student'
            elif(self.get_object().privacy == 'students'):
                student_shares = True
            return student_shares
           
        context['shares'] = shares()
        return context

class DetailCurrentStudent(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'detailStudent.html'

    login_url = 'login'

    def get_object(self):
        return get_object_or_404(Student, pk=self.request.session['_auth_user_id'])

# changeable student settings
class DetailStudentSettings(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'studentSettings.html'

    login_url = 'login'

class DetailCurrentStudentSettings(LoginRequiredMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'studentSettings.html'

    login_url = 'login'

    def get_object(self):
        return get_object_or_404(Student, pk=self.request.session['_auth_user_id'])
