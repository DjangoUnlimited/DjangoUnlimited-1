from django import forms
from django.core.exceptions import ValidationError
from django.forms import models, HiddenInput
from django.contrib.auth.models import User

from .models import Admin
# from ..DjangoUnlimited import settings

import dns.resolver, dns.exception

class InitialAdminForm(forms.ModelForm):
    
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(InitialAdminForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        if commit:
            user.save()
        return user

    def usernameExists(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            return True
        return False

    def emailExists(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            return True
        return False

    def emailDomainExists(self):
        email = self.cleaned_data.get("email")
        domain = email.split('@')[1]
        try:
            dns.resolver.query(domain, 'MX')
            return True

        except dns.exception.DNSException:
            return False

    def samePasswords(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        
        if p1 != p2:
            return False
        return True
        

class AdminForm(forms.ModelForm):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={'class': 'custom-select'}))

    class Meta:
        model = Admin
        exclude = ['user', 'admin_id']


class AddIndustryForm(forms.ModelForm):
    industry_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs=
                                                                                         {'class': 'form-control-text',
                                                                                          'style': 'resize:none;'}))
