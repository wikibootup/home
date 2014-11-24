from django.shortcuts import render
from django.http import HttpResponseRedirect, request
from users.models import User
from seeseehome import msg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from django.core.validators import validate_email

def signup(request):
    if request.method == 'POST':    
        ### username
        username = request.POST['username']

        ## username validator
        try:
            User.objects.validate_username(username)
        except ValidationError:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_invalid_name)

        ####
        ## username unique check
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_exist_name)
            
        ######
        ### email
        email = request.POST['email']
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_invalid_email)

        ####
        ## email unique check
        try:
            User.objects.get(email = email)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_exist_email)

        ######
        ### password
        password = request.POST['pwd']
        try:
            User.objects.validate_password(password)
        except ValidationError:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_invalid_pwd)
        ######
        ### User Registration
        User.objects.create_user(username = username, email = email,
                                password = password)

        messages.success(request, msg.users_signup_success)
        messages.info(request, msg.users_signup_success_info)

    return render(
               request,
               "users/signup.html",
           )

