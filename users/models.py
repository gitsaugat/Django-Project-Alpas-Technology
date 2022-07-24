from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Userprofile(models.Model):

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
