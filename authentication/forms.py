from django import forms
from django.contrib.auth.forms import AuthenticationForm

class ChukaiLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='仲介ユーザー名',
        widget=forms.TextInput(attrs={'placeholder': 'ユーザー名'})
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'})
    )
    client_id = forms.CharField(widget=forms.HiddenInput)

class BaibaiLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='売買用ユーザー名',
        widget=forms.TextInput(attrs={'placeholder': 'ユーザー名'})
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'})
    )
    client_id = forms.CharField(widget=forms.HiddenInput)
