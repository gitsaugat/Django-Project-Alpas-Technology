from django.shortcuts import redirect, render
from django.views import View
from .forms import LoginForm
from django.contrib.messages import error, success, warning
from django.contrib.auth import authenticate, login
# Create your views here.


class LoginView(View):

    def get(self, request):
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
        template_name = 'users/register.html'
        context = {
            'title': 'Register Page'
        }
        return render(request, template_name, context)

    def post(self, request):
        pass
