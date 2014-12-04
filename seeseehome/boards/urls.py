from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^boards/([0-9]+)/page/([0-9]+)/', 'boards.views.boardpage', 
        name="boardpage"), 
    url(r'^boards/([0-9]+)/post/([0-9]+)/', 'boards.views.postpage', 
        name="postpage"),
    url(r'^boards/([0-9]+)/post/$', 'boards.views.write', name="write"),
    url(r'^boards/([0-9]+)/post/([0-9]+)/rewrite/', 'boards.views.rewrite', 
        name="rewrite"),
) 
