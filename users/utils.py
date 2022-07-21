from django.contrib.auth.models import User


class UserValidation:

    def __init__(self, username, email, password, cpassword):

        self.username = username
        self.email = email
        self.password = password
        self.cpassword = cpassword

    def validate_username(self):
        user = User.objects.filter(username=self.username)
        if len(user) > 0:
            return False
        return True

    def validate_email(self):
        user = User.objects.filter(email=self.email)
        if len(user) > 0:
            return False
        return True

    def validate_password(self):
        if self.password == self.cpassword:
            self.confirmed_password = self.password
            return True

        return False

    def validate_password_length(self):
        if len(self.confirmed_password) > 7 and len(self.confirmed_password) <= 16:
            return True
        return False
