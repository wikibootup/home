from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
#   admin page
    url(r'^admin/', include(admin.site.urls), name="admin"),

#   main page
    url(r'^$', 'seeseehome.views.home', name='home'),

#   about us
    url(r'^aboutus/', 'seeseehome.views.aboutus', name='aboutus'),

#   ckeditor set
    url(r'^ckeditor/', include('ckeditor.urls')),

#   users' urls
    url(r'^', include('users.urls', namespace='users')),

#   boards' urls
    url(r'^', include('boards.urls', namespace='boards')),

#   linkboard' urls
    url(r'^', include('linkboard.urls', namespace='linkboard')),


)
