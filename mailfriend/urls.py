from django.conf.urls.defaults import *

from mailfriend.views import *
from django.views.generic.base import TemplateView

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
                       url(
    regex   = '^sent/$',
    view    = TemplateView.as_view(template_name='mailfriend/sent.html'),
    name    = 'mailfriend_sent',
  ),
)
