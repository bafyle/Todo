from django import forms
from django.contrib.auth.forms import UsernameField

class LoginAndRegisterForm(forms.Form):
    username = forms.CharField(max_length=10, min_length=3, strip=True, required=True)
    password = forms.CharField(strip=False, required=True)

