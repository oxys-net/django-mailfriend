# -*- coding:utf-8 -*-
from datetime import datetime
from optparse import make_option
from time import time

from django.core.management.base import BaseCommand
from django.conf import settings

from mailfriend.models import MailedItem


class Command(BaseCommand):
    """Delete old ``MailedItem``s"""
    help = __doc__

    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
            action='store_true',
            dest='dryrun',
            default=False,
            help='Count the number of elements that would be deleted, without actually doing it'),
        )

    def handle(self, *args, **options):
        dryrun = options['dryrun']
        
        limit = time() - settings.MAILEDITEM_MAX_AGE
        limit = datetime.fromtimestamp(limit)
        query = MailedItem.objects.filter(date_mailed__lte=limit)

        if dryrun:
            count = query.count()
            print 'Total count of items to be deleted: %d' % count
        else:
            query.delete()
