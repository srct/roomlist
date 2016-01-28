from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# yes, this is a joke
@register.filter(name='bc')
def bc(num):
    if num < 0:
        positive_value = str(abs(num))
        return "%s B.C." % (positive_value)
    else:
        return num


@register.filter(name='gender_icon')
def gender_icon(gender_name):
    icon_template = '<i class="fa fa-%s fa-fw"></i>'
    if gender_name == 'male':
        icon_tag = (icon_template % 'mars') + " Male"
    elif gender_name == 'female':
        icon_tag = (icon_template % 'venus') + " Female"
    elif gender_name == 'trans':
        icon_tag = (icon_template % 'transgender') + " Trans"
    elif gender_name == 'intersex':
        icon_tag = (icon_template % 'transgender-alt') + " Intersex"
    elif gender_name == 'genderless':
        icon_tag = (icon_template % 'genderless') + " Genderless"
    elif gender_name == 'other':
        icon_tag = (icon_template % 'mars-stroke-v') + " Other"
    return mark_safe(icon_tag)
