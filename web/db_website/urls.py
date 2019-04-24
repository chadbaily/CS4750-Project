from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.media, name='home'),
    url(r'^error/$', views.error, name='error'),

    # Actors
    url(r'^actors/edit/(?P<pk>[0-9]+)/submit/',
        views.update_actor, name='update_actor'),
    url(r'^actors/edit/(?P<pk>[0-9]+)/$',
        views.edit_actors, name='edit_actor'),
    url(r'^actors/create/submit/$', views.submit_create_actor,
        name='submit_create_actor'),
    url(r'^actors/create/$', views.create_actor, name='create_actor'),
    url(r'^actors/info/(?P<pk>[0-9]+)/$', views.info_actor, name='info_actor'),
    url(r'^actors/$', views.actors, name='actors'),
    url(r'^actors/export', views.export_actors, name='export_actors'),
    url(r'^actors/delete/(?P<pk>[0-9]+)/$',
        views.delete_actor, name='delete_actor'),

    # Crew
    url(r'^crews/edit/(?P<pk>[0-9]+)/submit/',
        views.update_crew, name='update_crew'),
    url(r'^crews/edit/(?P<pk>[0-9]+)/$', views.edit_crews, name='edit_crew'),
    url(r'^crews/delete/(?P<pk>[0-9]+)/$',
        views.delete_crew, name='delete_crew'),
    url(r'^crews/create/submit/$', views.submit_create_crew,
        name='submit_create_crew'),
    url(r'^crews/create/$', views.create_crew, name='create_crew'),
    url(r'^crews/info/(?P<pk>[0-9]+)/$', views.info_crew, name='info_crew'),
    url(r'^crews/export', views.export_crews, name='export_crews'),
    url(r'^crews/$', views.crews, name='crews'),

    # Media
    url(r'^media/edit/(?P<pk>[0-9]+)/submit/',
        views.update_media, name='update_media'),
    url(r'^media/edit/(?P<pk>[0-9]+)/$', views.edit_media, name='edit_media'),
    url(r'^media/delete/(?P<pk>[0-9]+)/$',
        views.delete_media, name='delete_media'),
    url(r'^media/info/(?P<pk>[0-9]+)/$', views.info_media, name='info_media'),
    url(r'^media/create/submit/$', views.submit_create_media,
        name='submit_create_media'),
    url(r'^media/create/$', views.create_media, name='create_media'),
    url(r'^media/export/', views.export_media, name='export_media'),
    url(r'^$', views.media, name='media'),

    # Memes
    url(r'^meme/edit/(?P<pk>[0-9]+)/submit/',
        views.update_meme, name='update_meme'),
    url(r'^meme/edit/(?P<pk>[0-9]+)/$', views.edit_meme, name='edit_meme'),
    url(r'^meme/delete/(?P<pk>[0-9]+)/$',
        views.delete_meme, name='delete_meme'),
    url(r'^meme/create/submit/$', views.submit_create_meme,
        name='submit_create_meme'),
    url(r'^meme/create/$', views.create_meme, name='create_meme'),
    url(r'^meme/export', views.export_meme, name='export_meme'),
    url(r'^meme/$', views.meme, name='meme'),

    # Login
    url(r'^login/submit/$', views.submit_login, name='submit_login'),
    url(r'^login/$', views.login, name='login'),

    # Logout
    url(r'^logout/$', views.logout, name='logout'),

    # Review
    url(r'^review/edit/(?P<pk>[0-9]+)/submit/$',
        views.update_review, name='update_review'),
    url(r'^review/edit/(?P<pk>[0-9]+)/$',
        views.edit_review, name='edit_review'),
    url(r'^review/delete/(?P<pk>[0-9]+)/$',
        views.delete_review, name='delete_review'),
    url(r'^review/create/submit/$', views.submit_review,
        name='submit_review'),
    url(r'^review/create/$', views.create_review, name='create_review'),
    url(r'^review/export', views.export_review, name='export_review'),
    url(r'^review/$', views.review, name='review'),

    # Refs
    url(r'^references/edit/(?P<pk>[0-9]+)/$', views.edit_reference, name='edit_reference'),
    url(r'^references/delete/(?P<pk>[0-9]+)/$', views.delete_reference, name='delete_reference'),
    url(r'^references/create/submit/$', views.submit_create_reference, name='submit_create_reference'),
    url(r'^references/create/$', views.create_reference, name='create_reference'),
    url(r'^references/export', views.export_refs, name='export_references'),
    url(r'^references/$', views.refs, name='references'),
]
