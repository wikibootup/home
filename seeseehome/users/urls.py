from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^signup/', 'users.views.signup', name="signup"),
    url(r'^login/', 'users.views.login', name="login"),
)

