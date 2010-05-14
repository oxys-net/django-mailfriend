from django.conf.urls.defaults import *

from mailfriend.views import *

urlpatterns = patterns('',
  url(
    regex   = '^(?P<content_type_id>\d+)/(?P<object_id>\d+)/$',
    view    = display_form,
    name    = 'mailfriend_form',
  ),
  url(
    regex   = '^send/$',
    view    = send,
    name    = 'mailfriend_send',
  ),
)
