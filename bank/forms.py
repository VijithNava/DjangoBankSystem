from django import forms
from models import Accounts
from django.utils.translation import ugettext as _
from django.contrib.auth import hashers
from django.contrib.auth.password_validation import validate_password
from sampler.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        data=self.cleaned_data['username']
        user_exists = User.objects.filter(username=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('Check User Name and Password'), code='invalid')
        return data

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user_profile = User.objects.get(username=username)
            if not username or not password or not hashers.check_password(password, user_profile.password):
                raise forms.ValidationError(_('Check User Name and Password'), code='invalid')

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        data=self.cleaned_data['email']
        user_exists = User.objects.filter(email=data).exists()
        if user_exists:
            raise forms.ValidationError(_('Email already exists'), code='invalid')
        return data

    def clean_username(self):
        data=self.cleaned_data['username']
        user_exists = User.objects.filter(username=data).exists()
        if user_exists:
            raise forms.ValidationError(_('User Name already exists'), code='invalid')
        return data

    def clean_password(self):
        data=self.cleaned_data['password']
        """
        Add validation rules for password.
        ie.
        1. Length of 8 or more
        2. Must have letters + numbers
        3. ...
        """
        validate_password(password=data)
        return data

class MoneyTransferForm(forms.Form):
    to_email = forms.EmailField()
    transfer_value = forms.DecimalField(min_value=0, localize=True, decimal_places=2)
    from_email = forms.EmailField(widget=forms.HiddenInput())

    def clean_from_email(self):
        data = self.cleaned_data['from_email']
        user_exists = User.objects.filter(email=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('Invalid email'), code='invalid')
        return data

    def clean_to_email(self):
        data = self.cleaned_data['to_email']
        user_exists = User.objects.filter(email=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('Invalid email'), code='invalid')
        return data

    def clean(self):
        cleaned_data = super(MoneyTransferForm, self).clean()
        from_email = cleaned_data.get("from_email")
        transfer_value = cleaned_data.get("transfer_value")
        if from_email and transfer_value:
            user_account = Accounts.objects.get(user__email=from_email)
            if not user_account.balance >= transfer_value:
                raise forms.ValidationError(_('Insufficient Balance'), code='invalid')


