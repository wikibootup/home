from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seeseehome.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'seeseehome.views.home', name='home'),

    # users' urls
    url(r'^', include('users.urls', namespace='users')),

    # boards' urls
    url(r'^', include('boards.urls', namespace='boards')),
)
