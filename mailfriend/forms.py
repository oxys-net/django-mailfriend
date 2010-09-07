from django import forms

from mailfriend.models import MailedItem
from django.utils.translation import ugettext_lazy as _

class MailedItemForm(forms.ModelForm):

    mailed_by_name = forms.CharField(label=_("Your name"), required=True)
    mailed_by_email = forms.EmailField(label=_("Your E-mail"))
    mailed_to = forms.EmailField(label=_("Recipient's E-mail"))
    user_email_as_from = forms.BooleanField(label=_("Use my e-mail address as from address"), required=False)
    send_to_user_also = forms.BooleanField(label=_("Send myself a copy of this e-mail"), required=False)
    error_css_class = "field-error"
    
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            user = kwargs.pop('user')
        else:
            user = None
        super(MailedItemForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated():
            initial_name = user.get_full_name() or user.username
            initial_email = user.email
        else:
            initial_name = ""
            initial_email = ""
        self.fields['mailed_by_name'].initial = initial_name
        self.fields['mailed_by_email'].initial = initial_email
        
        self.fields.keyOrder = [
            'mailed_by_name',
            'mailed_by_email',
            'mailed_to',
            'user_email_as_from',
            'send_to_user_also'
        ]
    
    def clean(self):
        if 'mailed_to' in self.cleaned_data and 'mailed_by_email' in self.cleaned_data:
            dst = self.cleaned_data['mailed_to']
            src = self.cleaned_data['mailed_by_email']
            content_type = self.instance.content_type
            object_pk = self.instance.object_pk
            
            if MailedItem.objects.filter(mailed_by_email=src, mailed_to=dst, object_pk=object_pk, content_type=content_type).count():
                raise forms.ValidationError(_("You already sent a mail to this address about the same content!"))

        return self.cleaned_data

    class Meta:
        model = MailedItem
        exclude = ('mailed_by', 'date_mailed', 'content_type', 'object_pk')
