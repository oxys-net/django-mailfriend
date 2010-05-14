from django import forms

from mailfriend.models import MailedItem

class MailedItemForm(forms.ModelForm):

    user_email_as_from = forms.BooleanField(label="Use my e-mail address as from address", required=False)
    send_to_user_also = forms.BooleanField(label="Send myself a copy of this e-mail", required=False)

    class Meta:
        model = MailedItem
        exclude = ('mailed_by', 'date_mailed', 'content_type', 'object_pk')
