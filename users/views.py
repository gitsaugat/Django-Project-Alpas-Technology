import profile
from urllib import request
from .models import Userprofile
from pyexpat.errors import messages
from readline import read_init_file
from django.shortcuts import redirect, render, HttpResponse
from django.urls import is_valid_path
from django.views import View
from .forms import LoginForm, RegisterForm, UserProfileForm
from django.contrib.messages import error, success, warning
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .utils import UserValidation
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

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
            first_name = form.cleaned_data.get('fname')
            last_name = form.cleaned_data.get('lname')
            validation = UserValidation(
                username, email, password, confirm_password)
            if validation.validate_email():
                if validation.validate_username():
                    if validation.validate_password():
                        if validation.validate_password_length():
                            newuser = User.objects.create(
                                username=username, email=email, first_name=first_name, last_name=last_name)

                            newuser.set_password(password)
                            newuser.save()
                            success(
                                request, f'Successfully Registered as {username}')
                            return redirect('/user/login')
                        error(
                            request, 'Password length must be greater than or equal to 8')
                    error(request, 'Password Validation Failed')
                error(request, 'Try a different username')
            error(request, 'User with the email exists')
        return redirect('/user/register')


class LogoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('/')


class PassworReset(View):
    def get(self, request):
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="users/password_reset.html", context={"form": password_reset_form})

    def post(self, request):
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


class UserProfileView(View):
    def get_full_name(self, id):
        user = User.objects.get(id=id)
        return f"{user.first_name} {user.last_name}"

    @method_decorator(login_required)
    def get(self, request):
        template_name = "users/update_profile.html"

        context = {
            'title': 'User Profile',
            'form': None,
            'full_name': self.get_full_name(request.user.id)
        }
        profiles = Userprofile.objects.filter(user=request.user)
        if len(profiles) > 0:
            context['form'] = UserProfileForm(instance=profiles[0])
            context['profile_exists'] = True
            context['profile'] = profiles[0]
        else:
            context['form'] = UserProfileForm()
        return render(request, template_name, context)

    def post(self, request):
        profiles = Userprofile.objects.filter(user=request.user)
        form = UserProfileForm(request.POST, request.FILES)

        if len(profiles) > 0:
            form = UserProfileForm(
                request.POST, request.FILES, instance=profiles[0])
        if form.is_valid():

            try:
                newuserprofilemodel = form.save(commit=False)
                newuserprofilemodel.user = request.user
                newuserprofilemodel.save()
                success(request, 'Updated !')
                return redirect('user_profile_view')
            except Exception as e:
                error(request, str(e))
                return redirect('user_profile_view')
        for err in form.errors:
            error(request, str(err))
        return redirect('user_profile_view')
