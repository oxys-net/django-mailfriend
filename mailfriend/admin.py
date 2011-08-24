from django.contrib import admin

from mailfriend.models import MailedItem


class MailedItemAdmin(admin.ModelAdmin):
    raw_id_fields = ('mailed_by',)
  
admin.site.register(MailedItem, MailedItemAdmin)
