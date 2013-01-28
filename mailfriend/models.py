import datetime

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class MailedItem(models.Model):
    # Content-object field
    content_type   = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_pk      = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    mailed_by = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True)
    mailed_by_email = models.EmailField("Sender's E-mail")
    mailed_to = models.EmailField("Recipient's E-mail")
    user_email_as_from = models.BooleanField(default=False)
    send_to_user_also = models.BooleanField(default=False)
    date_mailed = models.DateTimeField(default=datetime.datetime.now, editable=False)

    def __unicode__(self):
        return "%s: To %s, from %s" % (unicode(self.content_object), self.mailed_to, unicode(self.mailed_by or self.mailed_by_email))
