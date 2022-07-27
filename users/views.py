
from .models import Userprofile
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from .forms import LoginForm, RegisterForm, UserProfileForm, UpdatePasswordForm, EmailUpdateForm, UsernameUpdateForm, Personal
from django.contrib.messages import error, success, warning, get_messages
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
from core.views import PF_LG_DECO
from django.contrib.sessions.models import Session

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


class UsersSetting(View):
    @method_decorator(PF_LG_DECO)
    def get(self, request):
        print(request.session.keys())

        template_name = "users/settings.html"
        context = {
            'title': 'Settings',
            'username_form': UsernameUpdateForm(),
            'password_form': UpdatePasswordForm(),
            'email_form': EmailUpdateForm(),
            'personal_from': Personal()
        }
        return render(request, template_name, context)


class EmailResetView(View):
    @method_decorator(PF_LG_DECO)
    def post(self, request):
        email_form = EmailUpdateForm(request.POST)
        validator = UserValidation('', '', '', '')
        user = request.user
        if email_form.is_valid():
            email = email_form.cleaned_data.get('email')
            validator.email = email
            if validator.validate_email():
                user.email = email
                try:
                    user.save()
                    success(request, 'Email Updated')
                    return redirect('user_settings_view')
                except Exception as e:
                    error(request, str(e))
                    return redirect('user_settings_view')

            else:
                error(request, 'Try a different email')
                return redirect('user_settings_view')
        else:
            for er in email_form.errors:
                error(request, er)
            return redirect('user_settings_view')


class UsernameResetView(View):
    @method_decorator(PF_LG_DECO)
    def post(self, request):
        username_form = UsernameUpdateForm(request.POST)
        validator = UserValidation('', '', '', '')
        user = request.user
        if username_form.is_valid():

            username = username_form.cleaned_data.get('username')
            validator.username = username
            if validator.validate_username():
                try:
                    user.username = username
                    user.save()
                    success(request, 'Username Updated')
                    return redirect('user_settings_view')
                except Exception as e:
                    error(request, str(e))
                    return redirect('user_settings_view')

            else:
                error(request, 'Try a different username')
                return redirect('user_settings_view')
        else:
            for er in username_form.errors:
                error(request, er)
            return redirect('user_settings_view')


class PersonalNameView(View):
    @method_decorator(PF_LG_DECO)
    def post(self, request):
        personal_from = Personal(request.POST)
        user = User.objects.get(id=request.user.id)

        if personal_from.is_valid():
            fname = personal_from.cleaned_data.get('fname')
            lname = personal_from.cleaned_data.get('lname')

            user.first_name = fname
            user.last_name = lname
            try:
                user.save()
                success(request, 'Personal Information Updated')
                return redirect('user_settings_view')
            except Exception as e:
                error(request, str(e))
                print(e)
                return redirect('user_settings_view')
        else:
            for er in personal_from.errors:
                error(request, er)
            return redirect('user_settings_view')


class PasswordResetView(View):
    @method_decorator(PF_LG_DECO)
    def post(self, request):
        password_form = PasswordResetForm(request.POST)
        user = User.objects.get(id=request.user.id)
        validator = UserValidation('', '', '', '')
        if password_form.is_valid():
            password = password_form.cleaned_data.get('password')
            confirm_password = password_form.cleaned_data.get(
                'confirm_password')
            validator.confirmed_password = confirm_password
            validator.password = password
            if password == confirm_password:
                if validator.validate_password_length():
                    try:
                        user.set_password(password)
                        success(request, 'Password Updated')
                        return redirect('user_settings_view')
                    except Exception as e:
                        error(request, str(e))
                        return redirect('user_settings_view')
                else:
                    error(request, str(e))
                    return redirect('user_settings_view')

        else:
            for er in password_form.errors:
                error(request, er)
            return redirect('user_settings_view')
