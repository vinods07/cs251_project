from django.conf.urls import url,include
from django.contrib import admin
from . import views

app_name = 'index'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/first_login/$', views.first_login, name='first_login'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]
