from django.conf.urls import patterns, url

from bees.views import index, HiveView, SettingsView

urlpatterns = patterns('',
    url(r'^beekeeper/(?P<pk>\d+)/$', SettingsView.as_view(), name='beekeeper-settings'),
    url(r'^hive/(?P<pk>\d+)/$', HiveView.as_view(), name='hive-detail'),
    url(r'^$', index, name='index'),
)
