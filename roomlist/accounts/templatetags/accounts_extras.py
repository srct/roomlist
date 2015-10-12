from django import template

register = template.Library()


# yes, this is a joke
@register.filter(name='bc')
def bc(num):
    if num < 0:
        positive_value = str(abs(num))
        return "%s B.C." % (positive_value)
    else:
        return num
