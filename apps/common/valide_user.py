from django.contrib.auth.models import User
from django.core.validators import validate_email, EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


class ValideUserRegister:
    error_message = ""

    def is_username(self, username):
        """
            username doesn't exit before and length >=4
        """
        if (User.objects.filter(username=username).exists() == False):
            valid = (len(username)>4)
            if (valid):
                return True
            self.error_message += " username has more than 3 charactor "
            return False
        self.error_message += "exited user. "
        return False

    def is_email(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError as e:
            self.error_message += "wrong email. "
            return False

    def is_password(self, password):
        try:
            validate_password(password=password)
            return True
        except ValidationError as e:
            self.error_message += "wrong password. "
            return False

#todo: valid user login:
class ValideUserLogin:
    error_message = ""
    def is_exists(self,username):
        if (User.objects.filter(username=username).exists() == True):
            return True
        return False
