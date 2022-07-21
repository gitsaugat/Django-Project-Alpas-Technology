from os import umask
from urllib import request
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from .forms import LoginForm, RegisterForm
from django.contrib.messages import error, success, warning
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .utils import UserValidation
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from AlpasProject.settings import BASE_DIR
import os

# Create your views here.


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        template_name = 'users/login.html'
        context = {
            'title': 'Login Page',
            'form': LoginForm()
        }
        return render(request, template_name, context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                success(request, f'Welcome ,{user.username} ')
                return redirect('/')
            error(request, 'Username or Password invalid')

        return redirect('/user/login')


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        template_name = 'users/register.html'
        context = {
            'title': 'Register Page',
            'form': RegisterForm()
        }
        return render(request, template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            validation = UserValidation(
                username, email, password, confirm_password)
            if validation.validate_email():
                if validation.validate_username():
                    if validation.validate_password():
                        if validation.validate_password_length():
                            newuser = User.objects.create(
                                username=username, email=email)
                            newuser.set_password(password)
                            newuser.save()
                            success(
                                request, f'Successfully Registered as {username}')
                            return redirect('/user/login')
                        else:
                            error(
                                request, 'Password length must be greater than or equal to 8')
                    else:
                        error(request, 'Password Validation Failed')
                else:
                    error(request, 'Try a different username')
            else:
                error(request, 'User with the email exists')
        return redirect('/user/register')


class LogoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('/')


def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            user = User.objects.get(email=data)
            if user:

                subject = "Password Reset Requested"
                email_template_name = "users/txts/password_reset_email.txt"
                c = {
                    "email": user.email,
                    'domain': 'localhost:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.id)),

                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'admin@example.com',
                              [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="users/password_reset.html", context={"form": password_reset_form})
