from django import forms
from models import Accounts, UserProfile
from django.utils.translation import ugettext as _
from django.contrib.auth import hashers
from django.contrib.auth.password_validation import validate_password
from sampler.settings import AUTH_PASSWORD_VALIDATORS

class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_user_name(self):
        data=self.cleaned_data['user_name']
        user_exists = UserProfile.objects.filter(user_name=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('Check User Name and Password'), code='invalid')
        return data

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        user_name = cleaned_data.get("user_name")
        password = cleaned_data.get("password")
        user_profile = UserProfile.objects.get(user_name=user_name)
        if not user_name or not password or not hashers.check_password(password, user_profile.password):
            raise forms.ValidationError(_('Check User Name and Password'), code='invalid')

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    user_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        data=self.cleaned_data['email']
        user_exists = UserProfile.objects.filter(user_email=data).exists()
        if user_exists:
            raise forms.ValidationError(_('Email already exists'), code='invalid')
        return data

    def clean_user_name(self):
        data=self.cleaned_data['user_name']
        user_exists = UserProfile.objects.filter(user_name=data).exists()
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
        user_exists = UserProfile.objects.filter(user_email=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('Invalid email'), code='invalid')
        return data

    def clean_to_email(self):
        data = self.cleaned_data['to_email']
        user_exists = UserProfile.objects.filter(user_email=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('Invalid email'), code='invalid')
        return data

    def clean(self):
        cleaned_data = super(MoneyTransferForm, self).clean()
        from_email = cleaned_data.get("from_email")
        transfer_value = cleaned_data.get("transfer_value")

        if from_email and transfer_value:
            user_account = Accounts.objects.get(user__user_email=from_email)
            if not user_account.balance >= transfer_value:
                raise forms.ValidationError(_('Insufficient Balance'), code='invalid')


