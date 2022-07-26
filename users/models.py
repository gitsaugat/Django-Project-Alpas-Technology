from secrets import choice
from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

USER_ROLES = (
    ('VE', 'VENDOR'),
    ('CU', 'CUSTOMER')
)


class Userprofile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        default="default.jpg")
    country = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    telephone_no = models.CharField(max_length=200, null=True)
    mobile_no = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Roles(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class UserRoles(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.OneToOneField(Roles, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username + "'s role"


class UserActivity(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    brief = models.TextField()
    reference_model = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
