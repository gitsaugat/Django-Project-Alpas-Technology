from django.contrib.auth.models import User
import json
import uuid
import datetime


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


def get_err_data():
    try:
        with open('jsons/err.json', 'r') as stream:
            data = json.load(stream)
            stream.close()
        return data
    except Exception as e:
        print(e)


def write_err(err):
    try:
        with open('jsons/err.json', 'w') as stream:
            existing_Err_data = get_err_data()
            newdata = existing_Err_data['errors'].append({
                'id': uuid.uuid4(),
                'brief': err,
                'datetime': datetime.datetime.now()
            })

            json.dump(stream, newdata)
    except Exception as e:
        print(e)
