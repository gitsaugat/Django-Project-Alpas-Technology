from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=24, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=16, min_length=4)
