# -*- coding: utf-8 -*-

from django import forms
from bees.models import DUser


class DUserForm(forms.ModelForm):

    class Meta:
        model = DUser
        fields = ['d_id']
