# -*- coding: utf-8 -*-

import json
import datetime
from django.db import models
from django.utils.translation import ugettext as _

class DUser(models.Model):

    d_id = models.CharField(verbose_name=_('diary_user_id'), max_length=255,
                                blank=True, unique=True, default="")
    joined = models.DateTimeField(verbose_name=_('joined'), auto_now_add=True,
                                editable=False)
    last_visited = models.DateTimeField(verbose_name=_('last_visited'), blank=True,
                                editable=False, null=True)
    updated = models.DateTimeField(verbose_name=_('updated'), blank=True, null=True)
    bees = models.TextField(verbose_name=_('bees'), blank=True, default='')
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.d_id

    class Meta:
        verbose_name = _('diary user')
        verbose_name_plural = _('diary users')

    def update_bees(self, new_bees):
        old_bees = Bees(self.bees)
        new_bees = Bees(new_bees)
        if old_bees != new_bees:
            diff = old_bees.diff(new_bees)
            for d in diff:
                h = History.create_from_diff(d)
                h.duser = self
                h.save()
            self.bees = new_bees.to_json()
        self.updated = datetime.datetime.now()


class History(models.Model):

    action_choices = (
                      ('l', _('left')),
                      ('j', _('joined')),
                      ('r', _('renamed')),
                     )
    d_id = models.IntegerField()
    d_name = models.CharField(verbose_name=_('diary_user_name'), max_length=255)
    old_name = models.CharField(verbose_name=_('diary_old_user_name'),
                                max_length=255, blank=True, default="")
    action = models.CharField(choices=action_choices, max_length=25)
    when = models.DateTimeField(verbose_name=_('when'), auto_now_add=True,
                                editable=False)
    duser = models.ForeignKey('Duser')

    def __str__(self):
        return '{} {}'.format(self.d_name, self.action, self.when)

    class Meta:
        verbose_name = _('bee')
        verbose_name_plural = _('bees')
        ordering = ['-when']
        order_with_respect_to = 'duser'

    @classmethod
    def create_from_diff(cls, diff_tuple):
        '''
        Recieve tuple and return a History object.
        '''
        h = cls()
        h.d_id = int(diff_tuple[0])
        h.action = diff_tuple[1]
        h.d_name = diff_tuple[2]
        if len(diff_tuple) > 3:
            h.old_name = diff_tuple[3]
        return h

class Bees(object):
    '''
    Helper class to create bees_dict from either json or tuple.
    '''

    def __init__(self, smth):
        self._bees_dict = {}
        self.load(smth)

    def load(self, smth):
        if isinstance(smth, str):
            self._load_from_json(smth)
        if isinstance(smth, list):
            self._load_from_list(smth)

    def _load_from_json(self, smth):
        if not smth:
            smth = "{}"
        self._bees_dict = json.loads(smth)

    def _load_from_list(self, smth):
        self._bees_dict = {str(k): v for (k, v) in smth}

    def to_json(self):
        return json.dumps(self._bees_dict)

    def __eq__(self, other):
        return self._bees_dict == other._bees_dict

    def diff(self, other):
        diff = []
        for k in self._bees_dict:
            if k not in other._bees_dict:
                diff.append((k, 'l', self._bees_dict[k]))
            else:
                if self._bees_dict[k] != other._bees_dict[k]:
                    diff.append((k, 'r', self._bees_dict[k], other._bees_dict[k]))
        for k in other._bees_dict:
            if k not in self._bees_dict:
                diff.append((k, 'j', other._bees_dict[k]))
        return diff
