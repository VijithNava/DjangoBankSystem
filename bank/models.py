from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Accounts(models.Model):
    # This line is required. Links Accounts to a UserProfile model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    balance = models.DecimalField(decimal_places=2, max_digits=20)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
