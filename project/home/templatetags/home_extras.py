'''
Relevant Django docs:
https://docs.djangoproject.com/en/<VAR:DJANGO_VERSION>/howto/custom-template-tags/
'''
from django import template


register = template.Library()

@register.filter
def splitByFour(data):
    return [data[i:i+4] for i in range(0, len(data), 4)]
