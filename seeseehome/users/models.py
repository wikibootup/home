from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re
from django.db import OperationalError
from seeseehome import msg

class UserManager(BaseUserManager):
    def _create_user(self, username, email, 
                     password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        self.validate_username(username)
        email = self.normalize_email(email)
        validate_email(email)
        self.validate_password(password)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, 
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def validate_username(self, username):
        if not username:
            raise ValueError(msg.users_name_must_be_set)
        
        elif len(username) > 30:
            raise ValidationError(msg.users_name_at_most_30)
    
 
    def validate_password(self, password):
        if len(password) < 6:
            raise ValidationError(
                msg.users_pwd_at_least_6,
            )
        elif len(password) > 255:
            raise ValidationError(
                msg.users_pwd_at_most_255,
            )
        
        if bool(re.search('[0-9]', password)) is False:
            raise ValidationError(msg.users_pwd_no_numeric_char)
        
        if bool(re.search('[a-zA-Z]', password)) is False:
            raise ValidationError(msg.users_pwd_no_alphabet_char)
        
        if bool(re.search('[$&+,:;=?@#|\'\"<>.^*()%!-]', password)) is False:
            raise ValidationError(msg.users_pwd_no_special_char)
        
    def get_user(self, id):
        user = User.objects.get(id=id)
        return user


class User(AbstractBaseUser):
    objects = UserManager()
    USERNAME_FIELD = 'username'

    username = models.CharField(
               help_text = "User name",
               max_length = 30,
               unique = True,
               default = '',
           )
    email = models.EmailField(
                help_text = "User email",
                max_length = 64,
                unique = True,
                default = '',
            ) 

    is_active = models.BooleanField(
                    help_text = "Is active user?",
                    default=True
                )

    is_staff = models.BooleanField(
                   help_text = "Is the user can have access admin site?",
                   default=False
               )

    def deactivate(self):
        self.is_active = False
        return self.is_active

    def activate(self):
        self.is_active = True
        return self.is_active

