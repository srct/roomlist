# standard library imports
from __future__ import absolute_import, print_function
# third party imports
from haystack import indexes
# imports from your apps
from .models import Student


class StudentIndex(indexes.SearchIndex, indexes.Indexable):

    # search results
    # there can BE ONLY ONE document=True per model
    text = indexes.EdgeNgramField(document=True, use_template=True)
    # the use_template is in the app directory, just a text file
    # with the fields that we want to display when returning results

    # search filtering
    user = indexes.CharField(model_attr='user')

    def get_model(self):
        return Student

    def index_queryset(self, using=None):
        """When the entire index for model is updated."""
        return self.get_model().objects.all()
