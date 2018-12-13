import datetime
from django import forms
from .models import Event
from django_unixdatetimefield import UnixDateTimeField
from blogs.models import UserDetail
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class EventUploadForm(forms.ModelForm):
    # title = forms.CharField(max_length = 128)
    # image = forms.ImageField()
    # venue = forms.CharField(max_length = 128)
    # associatedClub = forms.CharField(max_length = 128)
    # description = forms.CharField(max_length = 500)
    # date = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #
    #     return cleaned_data
    class Meta:
        model = Event
