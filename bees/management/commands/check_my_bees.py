#!/usr/bin/env python
# encoding: utf-8

from django.core.management.base import BaseCommand, CommandError
from bees.utils import check_my_bees


class Command(BaseCommand):
    help = 'Grabs my bees and confirms all users, who are present'

    def handle(self, *args, **options):
        check_my_bees()
