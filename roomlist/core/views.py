# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.views.generic.base import ContextMixin


class StudentContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(StudentContextMixin, self).get_context_data(**kwargs)

        me = self.request.user.student

        context['student'] = me

        return context
