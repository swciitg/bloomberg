from django import template
from blogs.models import Blog

register = template.Library()

@register.filter('time_estimate')
def time_estimate(word_count):
    minutes = round(word_count/20)
    if minutes == 0:
        minutes =1 ;
    return minutes
