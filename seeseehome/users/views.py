from django.shortcuts import render
from django.http import HttpResponseRedirect, request
from users.models import User
from seeseehome import msg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from django.core.validators import validate_email
from django.core.urlresolvers import reverse

def delete_dicts(dicts):
    for dict_var in dicts:
        del dicts[dict_var]

def signup(request):
    ### username
    if request.method == 'POST':
        username = request.POST['username']
        ## username validator
        try:
            User.objects.validate_username(username)
        except ValidationError:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_invalid_name)
            delete_dicts(request.POST)
            return HttpResponseRedirect(reverse("users:signup"))
       
        ####
        ## username unique check
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_exist_name)
            return HttpResponseRedirect(reverse("users:signup"))
            
        ######
        ### email
        email = request.POST['email']
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_invalid_email)
            return HttpResponseRedirect(reverse("users:signup"))
       
        ####
        ## email unique check
        try:
            User.objects.get(email = email)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_exist_email)
            return HttpResponseRedirect(reverse("users:signup"))
      
        ######
        ### password
        password = request.POST['pwd']
        password_confirmation = request.POST['confirm_pwd']
    
        if password != password_confirmation:
            pass
    
        try:
            User.objects.validate_password(password)
        except ValidationError:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_invalid_pwd)
            return HttpResponseRedirect(reverse("users:signup"))
              
        ######
        ### User Registration
        User.objects.create_user(username = username, email = email,
                                password = password)
        
        messages.success(request, msg.users_signup_success)
        messages.info(request, msg.users_signup_success_info)
        return HttpResponseRedirect(reverse("users:signup"))

    return render(
               request,
               "users/signup.html",
           )

