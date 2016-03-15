from django.conf.urls import url

from . import views

app_name='bank'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^homepage/$', views.homepage, name='homepage'),
    url(r'^view_accounts/$', views.view_accounts, name='view_accounts'),
    url(r'^money_transfer/$', views.money_transfer, name='money_transfer'),
]

