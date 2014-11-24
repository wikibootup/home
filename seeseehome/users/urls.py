from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^signup/', 'users.views.signup', name="signup"),
    url(r'^login/', 'users.views.login', name="login"),
    url(r'^logout/', 'users.views.logout', name="logout"),
)

