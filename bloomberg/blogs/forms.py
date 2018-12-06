from django import forms
from .models import UserDetail
from passlib.hash import pbkdf2_sha256
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
    emailID = forms.EmailField(max_length = 100, widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder': 'Email'}),label ='Email')
    # password = forms.CharField(max_length=100, widget = forms.PasswordInput((attrs={'class': 'form-control' ,'placeholder': 'Type Your Password'}))
    password = forms.CharField(max_length = 100 , widget = forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder': 'Password'}),label ='Password')

    def clean(self):
        cleaned_data = super().clean()
        emailID = cleaned_data.get("emailID")
        password = cleaned_data.get("password")
        if UserDetail.objects.filter(emailID__exact = emailID):
            user = UserDetail.objects.get(emailID=emailID)
            if pbkdf2_sha256.verify(password, user.password):
                return cleaned_data
            else:
                raise ValidationError(_('Incorrect Password!') , code ='invalid')
        else:
            raise ValidationError(_('Email Id unregistered') , code ='invalid')
            # return False


class SignUpForm(forms.Form):
    name = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'class' : 'input-line full-width', 'placeholder': 'Username'}),label ='')
    emailID = forms.EmailField(max_length = 100, widget=forms.EmailInput(attrs={'class' : 'input-line full-width', 'placeholder': 'Email'}),label ='')
    mobile = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'input-line full-width', 'placeholder': 'Mobile'}),label ='')
    password = forms.CharField(max_length = 100 , widget = forms.PasswordInput(attrs={'class' : 'input-line full-width', 'placeholder': 'Password'}),label ='')


    def clean_emailID(self):
        data = self.cleaned_data['emailID']

        if UserDetail.objects.filter(emailID__exact = data):
            raise ValidationError(_('Email Id already registered') , code ='invalid')

        return data

    def clean_name(self):
        data = self.cleaned_data['name']

        return data

    def clean_password(self):
        data = self.cleaned_data['password']

        return data

    def clean_mobile(self):
        data = self.cleaned_data['mobile']

        return data

class BlogUploadForm(forms.Form):
    title = forms.CharField(max_length=128)
    image = forms.ImageField()
    content = forms.CharField(widget=forms.Textarea)
    topic = forms.CharField(max_length=100)
    tags = forms.CharField(max_length=30)
