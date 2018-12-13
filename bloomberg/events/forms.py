import datetime
from django import forms
from .models import Event
from blogs.models import UserDetail
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class EventUploadForm(forms.Form):
    title = forms.CharField(max_length = 128)
    image = forms.ImageField()
    venue = forms.CharField(max_length = 128)
    associatedClub = forms.CharField(max_length = 128)
    description = forms.CharField(max_length = 500)
    date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
