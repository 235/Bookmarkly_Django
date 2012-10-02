from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField()
    email = forms.EmailField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField()
