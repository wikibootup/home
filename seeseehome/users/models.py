from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re
from django.db import OperationalError
from seeseehome import msg

class UserManager(BaseUserManager):
##### CREATE
    def _create_user(self, username, email, password, 
        is_admin=False, **extra_fields):
        """ 
        It Creates and saves a User with the given username, email and 
        password.
        """
        self.validate_username(username)
        email = self.normalize_email(email)
        validate_email(email)
        self.validate_password(password)

        user = self.model(username=username, email=email, is_admin=is_admin)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, 
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, 
                is_admin=True, **extra_fields)
        return user

    def validate_username(self, username):
        if not username:
            raise ValueError(msg.users_name_must_be_set)
        elif len(username) > 30:
            raise ValidationError(msg.users_name_at_most_30)

        if bool(re.match('^[a-zA-Z0-9_-]+$', username)) is False:
            raise ValidationError(msg.users_invalid_name)    
 
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

    def validate_userperm(self, userperm):
        if userperm < 1:
            raise ValidationError(
                msg.users_userperm_at_least_1,
            )
        elif userperm > 31:
            raise ValidationError(
                msg.users_userperm_at_most_31,
            )
 

##########
##### RETRIEVE
    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
##########
##### UPDATE
    def update_user(self, id, **extra_fields):
        user = User.objects.get_user(id)
        if 'username' in extra_fields:
            self.validate_username(extra_fields['username'])
            user.username = extra_fields['username']

        if 'userperm' in extra_fields:
            self.validate_userperm(extra_fields['userperm'])
            user.userperm = extra_fields['userperm']

        if 'is_admin' in extra_fields:
            is_admin = extra_fields['is_admin']
            if type(is_admin) is bool:
                user.is_admin = is_admin
            else:
                raise ValidationError(
                        msg.users_update_is_admin_must_be_bool_type)

        user.save(using = self._db)

##########
##### DELETE        
    def delete_user(self, id):
        user = self.get(id=id)
        user.delete()

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

    """
    If you want your custom User model to also work with Admin, 
    your User model must define some additional attributes and methods.
    """
    is_admin = models.BooleanField(
                   help_text=('Is the user can access & edit admin page?'),
                   default=False,
                   )

    """
    admission_year = 
    """
    userperm = models.IntegerField(
                   help_text = "User permission ( user : 1, member : 2, "
                   "coremember : 4, graduate : 8, president : 16, all : 31 )",
                   default=msg.perm_user
               )

    def deactivate(self):
        self.is_active = False
        self.save()
        return self.is_active

    def activate(self):
        self.is_active = True
        self.save()
        return self.is_active

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_all_permissions(self, obj=None):
        if not self.is_active or self.is_anonymous() or obj is not None:
            return set()
        if not hasattr(self, '_perm_cache'):
            self._perm_cache = self.get_user_permissions(self)
            self._perm_cache.update(self.get_group_permissions(self))
        return self._perm_cache

    def has_module_perms(self, app_label):
        """
        Returns True if self has any permissions in the given app_label.
        """
        if not self.is_active:
            return False
        for perm in self.get_all_permissions(self):
            if perm[:perm.index('.')] == app_label:
                return True
        return False

