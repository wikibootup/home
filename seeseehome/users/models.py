from django.db import models
from django.contrib.auth.models import User, UserManager

class UserManager(UserManager):
    pass

class User(User):
    pass

