from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from collections import namedtuple
from django.db import transaction
from django.contrib.auth import hashers, authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
from django.http import HttpResponseRedirect

from .forms import RegisterForm, LoginForm, MoneyTransferForm
from .models import Accounts
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required
from sampler.settings import LOGIN_URL


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #validate form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #hash password before looking up in database against stored hashed password

            user_profile = get_object_or_404(User, username=username)
            #if 404 then display some error message while reloading loginpage (index)
            user = authenticate(username=username, password=password)
            # import pdb; pdb.set_trace()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('bank:homepage')
            else:
                form.add_error(None, ValidationError(_('Please check your log in credentials'), code='invalid'))
    else:
        form = LoginForm()
    return render(request=request, template_name='bank/index.html', context={'form': form})


def register(request):
    # display_info = namedtuple('display_info', ['display_name', 'field_name', 'input_type'])
    # display_infos = (
    #     display_info('User Name', 'username', 'text'),
    #     display_info('First Name', 'firstname', 'text'),
    #     display_info('Last Name', 'lastname', 'text'),
    #     display_info('Email', 'email', 'text'),
    #     display_info('Password', 'password', 'password'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            #create DB instance for user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password'] #remember to hash both email and password for storing.. this is just test
            user_profile = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password)
            #import pdb; pdb.set_trace()
            user_profile.save()
            account = Accounts(user=user_profile, balance=100) #instantiate user Account with 100$
            account.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('bank:homepage')
    else:
        form = RegisterForm()

    return render(request=request, template_name='bank/register.html', context={'form': form})


@login_required(login_url=LOGIN_URL)
def homepage(request):
    user_account = get_object_or_404(Accounts, user=request.user)
    user_profile = user_account.user
    return render(request=request, template_name='bank/homepage.html',
                  context={'user_profile': user_profile, 'user_account': user_account})


@login_required(login_url=LOGIN_URL)
def view_accounts(request):
    accounts = Accounts.objects.exclude(user=request.user)
    return render(request=request, template_name='bank/accounts.html',
                  context={'accounts': accounts})


@login_required(login_url=LOGIN_URL)
def money_transfer(request):
    user_account = get_object_or_404(Accounts, user=request.user)
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST)
        with transaction.atomic():
            if form.is_valid():
                transfer_value = form.cleaned_data['transfer_value']
                recipient_email = form.cleaned_data['to_email']
                user_account.balance -= transfer_value
                user_account.save()
                recipient_account = Accounts.objects.get(user__email=recipient_email)
                recipient_account.balance += transfer_value
                recipient_account.save()
                return redirect('bank:homepage')
    else:
        form = MoneyTransferForm()

    return render(request=request, template_name='bank/transfer.html', context={'form': form, 'email': user_account.user.email})


def sign_out(request):
    logout(request)
    return redirect('bank:index')
