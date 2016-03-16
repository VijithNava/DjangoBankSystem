# DjangoBankSystem

###Problem 
Create a Banking Application with the following requirements:
- User can Sign Up (registration) form: first name, last name, email, password and confirm password. Validate password to be sure it's strong enough (the rules are up to you). No need to send confirmation email. Once account is registered, user should get $100 on his account.
- User can Sign In and see his profile information as well as his balance. 
- User can Sign Out.
- User can see all the other users in the system and their balances.
- Each user can transfer any amount to any other user.

##Install Instructions

###Install Python and PIP
[install python](https://www.python.org/downloads/release/python-2710/)

[install pip] (https://pip.pypa.io/en/stable/installing/) 

**Note: pip is already installed if you're using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from python.org, but you'll need to upgrade pip.**


###Install Application
1. Download repository to local directory (ie. <_local_dir_> )
2. Set present working directory to point to <_local_dir_>
3. Enter in terminal:
```
pip install -r requirements.txt
```

##Run Application
1. From terminal, run the following command to start the local server
```
python manage.py runserver
```
2. Open your favourite browser and enter this local end point:
```
http://127.0.0.1:8000/bank/
```
