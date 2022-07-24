from django import forms
from .models import Userprofile


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=24, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=16, min_length=4)


class RegisterForm(forms.Form):
    fname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=24, min_length=3)
    lname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=24, min_length=3)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=24, min_length=3)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=40, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=16, min_length=4)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=16, min_length=4)


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Userprofile
        fields = '__all__'
        exclude = ['user']


class UpdatePasswordForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=16, min_length=4)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=16, min_length=4)


class UsernameUpdateForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=24, min_length=3)


class EmailUpdateForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=40, min_length=3)


class Personal(forms.Form):

    fname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=24, min_length=3)
    lname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'form2Example1'}), max_length=24, min_length=3)
