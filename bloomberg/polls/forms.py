from django import forms
from polls.models import Question , Choice
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class PollForm(forms.Form):
    question = forms.CharField(max_length=200)
    choice_1 = forms.CharField(max_length=200)
    choice_2 = forms.CharField(max_length=200)
    choice_3 = forms.CharField(max_length=200,required=False)
    choice_4 = forms.CharField(max_length=200,required=False)

class ExitPollForm(forms.Form):
    question = forms.CharField(max_length=200)
    contestingPost = forms.CharField(max_length=50)
    candidate_1 = forms.CharField(max_length=100)
    candidate_2 = forms.CharField(max_length=100)
    candidate_3 = forms.CharField(max_length=100,required=False)
    candidate_4 = forms.CharField(max_length=100,required=False)
    candidate_5 = forms.CharField(max_length=100,required=False)
    candidate_6 = forms.CharField(max_length=100,required=False)
