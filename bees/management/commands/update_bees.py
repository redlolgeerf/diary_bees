#!/usr/bin/env python
# encoding: utf-8

from django.core.management.base import BaseCommand, CommandError
from bees.utils import update_bees


class Command(BaseCommand):
    help = 'Updates bees'

    def handle(self, *args, **options):
        update_bees()
