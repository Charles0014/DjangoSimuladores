from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', 'control.views.control_send', name='control_send'),
    url(r'^$','control.views.control_send', name='control_send'),
    url(r'^control/$', 'control.views.control_send', name='control_send'),
)
