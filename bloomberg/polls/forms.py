from django import forms
from polls.models import Question , Choice
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class PollForm(forms.Form):
    question = forms.CharField(max_length=200)
    choice1 = forms.CharField(max_length=200)
    choice2 = forms.CharField(max_length=200)
    choice3 = forms.CharField(max_length=200,required=False)
    choice4 = forms.CharField(max_length=200,required=False)
