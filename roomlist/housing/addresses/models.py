# core django imports
from django.db import models
# third party imports
from localflavor.us.models import USStateField, USZipCodeField
from model_utils.models import TimeStampedModel


# buildings on campus don't have separate addresses yet
class Address(TimeStampedModel):

    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = USStateField()
    zip_code = USZipCodeField()

    class Meta:
        verbose_name_plural = 'addresses'

    def __str__(self):              # __unicode__ on Python 2
        return ', '.join(self.street, self.city, self.state)
