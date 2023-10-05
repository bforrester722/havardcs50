
from django import template


register = template.Library()
import logging

logger = logging.getLogger("django")

@register.filter(name='is_in_list')
def is_in_list(value, given_list):

    return given_list.filter(username=value).exists() 
