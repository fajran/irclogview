from django.conf.urls.defaults import *

urlpatterns = patterns('irclogview.views',
    url(r'^(?P<name>[^/]+)/(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})/$', 'show_log', name='irclogview_show'),
    url(r'^(?P<name>[^/]+)/$', 'channel_index', name='irclogview_channel'),
    url(r'^$', 'index', name='irclogview_index'),
)

