from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^actors/edit/(?P<pk>[0-9]+)/submit/', views.update_actor, name='update_actor'),
    url(r'^actors/edit/(?P<pk>[0-9]+)/$', views.edit_actors, name='edit_actor'),
    url(r'^actors/$', views.actors, name='actors'),
]
