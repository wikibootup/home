from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from users.models import User
from seeseehome import msg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from django.core.validators import validate_email
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login

# I couldn't solve built-in authenticate problem yet
# So I use custom authenticate(But It is same as built-in authenticate)
def authenticate(username=None, password=None):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None

def delete_dicts(dicts):
    for dict_var in dicts:
        del dicts[dict_var]

def login(request):
    ### username
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pwd']
        user = authenticate(username = username, password = password)
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            if user.is_active:
                auth_login(request, user)
                messages.success(request, msg.users_login_success)
                messages.info(request, msg.users_login_success_info)
    
                next = ""
                if 'next' in request.GET:
                    next = request.GET['next']

                if next == "":
                    return HttpResponseRedirect(reverse("home"))
                else:
                    return HttpResponseRedirect(next)
        else:
            messages.error(request, msg.users_login_error)
            messages.info(request, msg.users_invalid)
            return HttpResponseRedirect(reverse("users:login"))
 
    return render(request, "users/login.html")
 
def signup(request):
    ### username
    if request.method == 'POST':
        username = request.POST['username']
        ## username validator
        try:
            User.objects.validate_username(username)
        except ValidationError:
          message.error(request, msg.users_signup_error)
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
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_confirm_pwd_error)
            return HttpResponseRedirect(reverse("users:signup"))

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
        return HttpResponseRedirect(reverse("users:login"))

    return render(request, "users/signup.html")

