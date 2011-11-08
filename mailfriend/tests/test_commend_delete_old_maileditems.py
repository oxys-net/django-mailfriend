import datetime
from time import time

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from django.conf import settings

from mailfriend.tests import DummyModel

from mailfriend.models import MailedItem




class TestCleanDeletedMessages(TestCase):

    def call_delete_old_maileditems_command(self, dryrun=False):
        call_command('delete_old_maileditems', dryrun=dryrun)

    def setUp(self):
        self.user = User.objects.create_user(
            username='mailfriend_test_user',
            email='mailfriend_test_user@example.com',
            password='123456'
        )
        
        dummy_object = DummyModel()
        dummy_object.save()
        MailedItem(
            content_object=dummy_object,
            mailed_by = self.user,
            mailed_to = 'friend@example.net'
        ).save()

    def test_dry_run(self):
        """If --dry_run is prodived don't delete"""
        # FIXME: override settings with django 1.4
        settings.MAILEDITEM_MAX_AGE = 0
        
        self.call_delete_old_maileditems_command(dryrun=True)
        
        self.assertEqual(1, MailedItem.objects.count())

    def test_delete_old_enough(self):
        """If the object is old enough, it's deleted"""
        settings.MAILEDITEM_MAX_AGE = 0
        
        self.call_delete_old_maileditems_command()
        
        self.assertEqual(0, MailedItem.objects.count())

    def test_delete_too_young(self):
        """If the object is too young, it's not deleted"""
        settings.MAILEDITEM_MAX_AGE = 999
        
        self.call_delete_old_maileditems_command()
        
        self.assertEqual(1, MailedItem.objects.count())
        
