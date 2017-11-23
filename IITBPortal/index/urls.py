from django.conf.urls import url,include
from django.contrib import admin
from . import views

app_name = 'index'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^refresh_feed/$', views.refresh_feed, name='refresh_feed'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/profile_pic/$', views.update_profile_pic, name='update_profile_pic'),
    url(r'^profile/update_profile/$', views.update_profile, name='update_profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/first_login/$', views.first_login, name='first_login'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^course/$', views.registered_courses, name='registered_courses'),
    url(r'^course/(?P<course_id>[0-9]+)/$', views.course, name='course'),

    url(r'^course/(?P<course_id>[0-9]+)/add_topic/$', views.add_topic, name='add_topic'),

    url(r'^profile/update_profile/$', views.update_profile, name='update_profile'),
    url(r'^profile/add_interests/$', views.add_interests, name='add_interests'),
    url(r'^profile/update_interests/$', views.update_interests, name='update_interests'),
    url(r'^all_courses/$', views.all_courses, name='all_courses'),
    url(r'^course_info/(?P<course_id>[0-9]+)/$', views.course_info, name='course_info'),
    url(r'^register_course/(?P<course_id>[0-9]+)/$', views.register_course, name='register_course'),
    url(r'^update_topic_assignment/(?P<topic_id>.*)/$', views.add_assignment, name='add_assignment'),
    url(r'^update_topic_material/(?P<topic_id>.*)/$', views.add_course_material, name='add_course_material'),
    url(r'^take_quiz/(?P<quiz_id>.*)/$', views.take_quiz, name='take_quiz'),
    url(r'^update_topic_resourse/(?P<topic_id>.*)/$', views.add_resourse, name='add_resourse'),

    url(r'^course/add_quiz/(?P<topic_id>[0-9]+)/$', views.add_quiz, name='add_quiz'),

    url(r'^course/add_another_question/(?P<quiz_id>[0-9]+)/$', views.add_another_question, name='add_another_question'),

    url(r'^course/take_quiz/(?P<quiz_id>[0-9]+)/$', views.take_quiz, name='take_quiz'),
    url(r'^course/add_question/(?P<topic_id>[0-9]+)/(?P<quiz_id>[0-9]+)/$', views.add_question, name='add_question'),

    url(r'^course/evaluate_quiz/(?P<quiz_id>[0-9]+)/$', views.evaluate_quiz, name='evaluate_quiz'),

    url(r'^course/result/(?P<quiz_id>[0-9]+)/$', views.result, name='result'),

]
