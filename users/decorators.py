from functools import wraps
from .models import UserActivity
from .utils import write_err


def user_activity_tracker(func):
    @wraps(func)
    def wrapped_function(request, *args, **kwargs):
        try:
            UserActivity.objects.create(
                user=request.user,
                brief=kwargs['brief'],
                referenced_model=kwargs['referenced_model']
            ).save()
        except Exception as e:
            write_err(str(e))
        return func(request, *args, **kwargs)
    return wrapped_function
