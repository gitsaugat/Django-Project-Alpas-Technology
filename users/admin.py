from django.contrib import admin
from .models import (
    Userprofile,
    UserRoles,
    UserActivity,
    Roles
)


# Register your models here.

admin.site.register(Userprofile)
admin.site.register(UserRoles)
admin.site.register(UserActivity)
admin.site.register(Roles)
