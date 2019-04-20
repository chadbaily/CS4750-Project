from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    
    url(r'^actors/edit/(?P<pk>[0-9]+)/submit/', views.update_actor, name='update_actor'),
    url(r'^actors/edit/(?P<pk>[0-9]+)/$', views.edit_actors, name='edit_actor'),
    url(r'^actors/create/submit/$', views.submit_create_actor, name='submit_create_actor'),
    url(r'^actors/create/$', views.create_actor, name='create_actor'),
    url(r'^actors/$', views.actors, name='actors'),

    url(r'^crews/edit/(?P<pk>[0-9]+)/submit/', views.update_crew, name='update_crew'),
    url(r'^crews/edit/(?P<pk>[0-9]+)/$', views.edit_crews, name='edit_crew'),
    url(r'^crews/create/submit/$', views.submit_create_crew, name='submit_create_crew'),
    url(r'^crews/create/$', views.create_crew, name='create_crew'),
    url(r'^crews/$', views.crews, name='crews'),

    url(r'^media/edit/(?P<pk>[0-9]+)/submit/', views.update_media, name='update_media'),
    url(r'^media/edit/(?P<pk>[0-9]+)/$', views.edit_media, name='edit_media'),
    url(r'^media/create/submit/$', views.submit_create_media, name='submit_create_media'),
    url(r'^media/create/$', views.create_media, name='create_media'),
    url(r'^media/$', views.media, name='media'),
]
