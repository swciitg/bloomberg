from django import template
from blogs.models import Blog

register = template.Library()

@register.filter('time_estimate')
def time_estimate(word_count):
    minutes = round(word_count/20)
    if minutes == 0:
        minutes =1 ;
    return minutes

@register.simple_tag()
def votes_percentage(vote,total):
    percent = vote*100
    percent/=total
    return percent

@register.simple_tag()
def rest_votes_percentage(vote,total):
    percent = (total-vote)*100
    percent/=total
    return percent

@register.filter
def get_at_index(list, index):
    return list[index]
