# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _

class DUser(models.Model):

    d_login = models.CharField(verbose_name=_('diary_user_name'), max_length=255,
                                blank=True, unique=True)
    joined = models.DateTimeField(verbose_name=_('joined'), auto_now_add=True,
                                editable=False)
    last_visited = models.DateTimeField(verbose_name=_('last_visited'), blank=True,
                                editable=False)
    updated = models.DateTimeField(verbose_name=_('updated'), blank=True)
    bees = models.TextField(verbose_name=_('bees'), blank=True)

    def __str__(self):
        return self.d_login

    class Meta:
        verbose_name = _('diary user')
        verbose_name_plural = _('diary users')

class History(models.Model):

    action_choices = (
                      ('l', _('left')),
                      ('j', _('joined')),
                      ('r', _('renamed')),
                     )
    d_id = models.IntegerField()
    d_name = models.CharField(verbose_name=_('diary_user_name'), max_length=255)
    old_name = models.CharField(verbose_name=_('diary_old_user_name'),
                                max_length=255, blank=True)
    action = models.CharField(choices=action_choices, max_length=25)
    when = models.DateTimeField(verbose_name=_('when'), auto_now_add=True,
                                editable=False)
    duser = models.ForeignKey('Duser')

    def __str__(self):
        return '{} {}'.format(self.d_name, self.action)

    class Meta:
        verbose_name = _('bee')
        verbose_name_plural = _('bees')
        ordering = ['-when']
        order_with_respect_to = 'duser'
