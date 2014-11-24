from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from seeseehome.views import Home

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seeseehome.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login_required(Home.as_view()), name='home'),

    # users' urls
    url(r'^', include('users.urls', namespace='users')),
)
