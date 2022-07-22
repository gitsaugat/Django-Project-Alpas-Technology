from functools import wraps
from django.contrib.messages import warning
from django.shortcuts import redirect
from users.models import Userprofile


def profile_required(func):
    @wraps(func)
    def wrapper_func(request, *args, **kwargs):
        try:
            Userprofile.objects.get(user=request.user)
            print(args, kwargs)

        except Userprofile.DoesNotExist as e:
            warning(request, 'Please setup your profile to move further !!')
            return redirect('user_profile_view')
        # Do something after the function.
        return func(request, *args, **kwargs)
    return wrapper_func
