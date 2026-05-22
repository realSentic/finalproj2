from django.contrib.auth.hashers import make_password
from django import forms
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from .models import Admins

class RegisterForm(forms.ModelForm):
    registration_key = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Admins
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_registration_key(self):
        key = self.cleaned_data.get('registration_key')
        if key != settings.REGISTRATION_KEY:
            raise forms.ValidationError('Invalid registration key.')
        return key

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def save(self, commit=True):
        admin = super().save(commit=False)
        admin.password = make_password(self.cleaned_data['password'])
        if commit:
            admin.save()
        return admin


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())