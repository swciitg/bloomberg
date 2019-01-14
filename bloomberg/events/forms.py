import datetime
from django import forms
from .models import Event
from main.models import UserDetail
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class EventUploadForm(forms.Form):
    title = forms.CharField(max_length = 128,widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder':'Event Name'}),label='title')
    image = forms.ImageField()
    venue = forms.CharField(max_length = 128,widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder':'Venue'}),label='Venue')
    associatedClub = forms.CharField(max_length = 128,widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder':'club name'}),label='Club Name')
    description = forms.CharField(max_length = 500,widget=forms.TextInput(attrs={'class' : 'form-control' , 'placeholder':''}),label='Description')
    date = forms.DateField(input_formats=['%d/%m/%Y'],widget=forms.widgets.DateInput(format="%d/%m/%Y",attrs={'class' : 'form-control' , 'placeholder':'dd/mm/yyyy'}),label='Date')

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
