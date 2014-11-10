#!/usr/bin/env python
# encoding: utf-8

from django.core.management.base import BaseCommand, CommandError
from bees.models import DUser
from bees.grabber import Grabber

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        diary_users = DUser.objects.all()
        grab = Grabber()
        for d_user in diary_users:
            new_bees = grab.get_bees(d_user.d_id)
            d_user.update_bees(new_bees)
            d_user.save()

