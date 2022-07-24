from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from .decorators import profile_required
# Create your views here.

PF_LG_DECO = [login_required, profile_required]


class HomeView(View):
    @method_decorator(PF_LG_DECO)
    def get(self, request):
        template_name = 'core/home.html'
        context = {
            'title': 'Homepage'
        }
        return render(request, template_name, context)
