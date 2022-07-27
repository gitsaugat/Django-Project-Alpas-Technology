from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import profile_required
from users.models import UserRoles
from django_otp.decorators import otp_required

# Create your views here.

PF_LG_DECO = [login_required, profile_required]


class HomeView(View):
    @method_decorator(PF_LG_DECO)
    def get(self, request):
        try:
            userrole = UserRoles.objects.get(user=request.user)
            if userrole.role.title.lower() == "vendor":
                return redirect('vendors_dashboard')
            if userrole.roles.title.lower() == "customer":
                return redirect('customers_dashboard')
        except UserRoles.DoesNotExist:
            template_name = 'core/home.html'
            context = {
                'title': 'Homepage'
            }
            return render(request, template_name, context)
