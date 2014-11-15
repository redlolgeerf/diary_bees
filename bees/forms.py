# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from bees.models import DUser


class DUserForm(forms.ModelForm):

    class Meta:
        model = DUser
        fields = ['d_id']

    def clean_d_id(self):
        data = self.cleaned_data['d_id']
        data = data.strip()
        if not data.isdigit():
            raise forms.ValidationError(
                    _('Diary id can be only numbers'))
        return data
