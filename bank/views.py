from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from collections import namedtuple
from django.db import transaction
from django.contrib.auth import hashers

# Create your views here.
from django.http import HttpResponseRedirect

from .forms import RegisterForm, LoginForm, MoneyTransferForm
from .models import  UserProfile, Accounts


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #validate form
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            #hash password before looking up in database against stored hashed password

            user_profile = get_object_or_404(UserProfile, user_name=user_name)
            #if 404 then display some error message while reloading loginpage (index)
            request.session['user_id'] = user_profile.id
            return redirect('bank:homepage')
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
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            password = hashers.make_password(form.cleaned_data['password']) #remember to hash both email and password for storing.. this is just test
            user_profile = UserProfile(first_name=first_name,
                               last_name=last_name,
                               user_name=user_name,
                               user_email=email,
                               password=password)
            user_profile.save()
            account = Accounts(user=user_profile, balance=100) #instantiate user Account with 100$
            account.save()
            request.session['user_id'] = user_profile.id
            return redirect('bank:homepage')
    else:
        form = RegisterForm()

    return render(request=request, template_name='bank/register.html', context={'form': form})


def homepage(request):
    #import pdb; pdb.set_trace()
    user_id = request.session['user_id']
    user_account = get_object_or_404(Accounts, pk=user_id)
    user_profile = user_account.user
    return render(request=request, template_name='bank/homepage.html',
                  context={'user_profile': user_profile, 'user_account': user_account})


def view_accounts(request):
    user_id = request.session['user_id']
    accounts = Accounts.objects.exclude(pk=user_id)

    return render(request=request, template_name='bank/accounts.html',
                  context={'accounts': accounts})

def money_transfer(request):
    user_id = request.session['user_id']
    user_account = get_object_or_404(Accounts, pk=user_id)
    import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST)
        with transaction.atomic():
            if form.is_valid():
                transfer_value=form.cleaned_data['transfer_value']
                recipient_email = form.cleaned_data['to_email']
                user_account.balance-=transfer_value
                user_account.save()
                recipient_account= Accounts.objects.get(user__user_email= recipient_email)
                recipient_account.balance+=transfer_value
                recipient_account.save()
        return redirect('bank:homepage')
    else:
        form = MoneyTransferForm()

    return render(request=request, template_name='bank/transfer.html', context={'form': form, 'user_email': user_account.user.user_email})


def signout(request):
    return redirect('bank:index')
