# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    email = forms.CharField(help_text="Email")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Пароль")
    password_repeat = forms.CharField(widget=forms.PasswordInput(),
                      help_text="Введите пароль ещё раз")

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            us = User.objects.get(email=data)
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        except User.DoesNotExist:
            pass
        return data

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')

        if password != password_repeat:
            msg = "Введённые пароли должны совпадать."
            self._errors["password"] = self.error_class([msg])
            del cleaned_data["password"]
            del cleaned_data["password_repeat"]
        return cleaned_data

    class Meta:
        model = User
        fields = ['email', 'password', 'password_repeat']

