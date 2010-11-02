import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.http import Http404
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext, loader, Context
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

# If django-mailer (http://code.google.com/p/django-mailer/) is available,
# favor it. Otherwise, just use django.core.mail. Thanks to brosner for the
# suggestion (you can also blame him if this doesn't work. Joking. Sort of.)
try:
    from mailer import send_mail
except ImportError:
    from django.core.mail import send_mail

from mailfriend.models import MailedItem
from mailfriend.forms import MailedItemForm

require_login = getattr(settings, "MAILFRIEND_REQUIRE_LOGIN", True)

def _get_templates(obj, name):
    prefix = obj.__class__.__name__.lower()
    return ('mailfriend/%s_%s.html' % (prefix, name), 'mailfriend/%s.html' % (name, ))

def display_form(request, content_type_id, object_id, form_class=MailedItemForm):
    content_type = ContentType.objects.get(pk=content_type_id)
    try:
        obj = content_type.get_object_for_this_type(pk=object_id)
        obj_url = obj.get_absolute_url()
    except ObjectDoesNotExist:
        raise Http404, "Invalid -- the object ID was invalid"
    form = form_class(user=request.user)
    context = {
      'content_type': content_type,
      'form': form,
      'object': obj,
    }
    return render_to_response(_get_templates(obj, "form"), context, context_instance=RequestContext(request))
if require_login:
    display_form = login_required(display_form)

def send(request, form_class=MailedItemForm):
    if not request.POST:
        raise Http404, "Only POSTs are allowed"
    content_type = ContentType.objects.get(pk=int(request.POST['content_type_id']))
    try:
        obj = content_type.get_object_for_this_type(pk=int(request.POST['object_pk']))
        obj_url = obj.get_absolute_url()
    except ObjectDoesNotExist:
        raise Http404, "The send to friend form had an invalid 'target' parameter -- the object ID was invalid"
    user = request.user.is_authenticated() and request.user or None
    mailed_item = MailedItem(mailed_by=user, content_type=content_type, object_pk=obj.pk)
    form = form_class(request.POST, instance=mailed_item)
    if form.is_valid():
        site = Site.objects.get_current()
        site_url = 'http://%s/' % site.domain
        url_to_mail = 'http://%s%s' % (site.domain, obj_url)
        mailed_by = form.cleaned_data['mailed_by_name']
        if hasattr(settings, 'MAILFRIEND_SUBJECT'):
            subject = settings.MAILFRIEND_SUBJECT % { 'user' : mailed_by }
        else:
            subject = _("You have received a link from %(user)s") % { 'user' : mailed_by }
        message_template = loader.get_template('mailfriend/email_message.txt')
        message_context = Context({ 
          'site': site,
          'site_url': site_url,
          'object': obj,
          'url_to_mail': url_to_mail,
          'mailed_by_name': mailed_by
        })
        message = message_template.render(message_context)
        recipient_list = [request.POST['mailed_to']]
        mailed_by_email = form.cleaned_data['mailed_by_email']
        if request.POST.has_key('send_to_user_also'):
            recipient_list.append(mailed_by_email)
        if request.POST.has_key('user_email_as_from'):
            from_address = mailed_by_email
        else:
            from_address = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_address, recipient_list, fail_silently=False)
        new_mailed_item = form.save()
        templates = _get_templates(obj, "sent")
    else:
        templates = _get_templates(obj, "form")
    return render_to_response(templates, {
                'object': obj, 
                'form' : form, 
                'content_type' : content_type 
    }, context_instance=RequestContext(request))
if require_login:
    send = login_required(send)
