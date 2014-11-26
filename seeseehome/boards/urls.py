from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^boardlist/', 'boards.views.boardlist', name="boardlist"),
    url(r'^boards/([0-9]+)/$', 'boards.views.boardpage', name="boardpage"), 
    url(r'^boards/([0-9]+)/posts/([0-9]+)/$', 'boards.views.postpage', 
        name="postpage"),

) 
