from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from seeseehome import msg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from linkboard.models import LinkPost
from users.models import User

def pagination_of_linkboard(posts, posts_per_page=10, page=1):
#   posts per page
    start_pos = (int(page)-1) * posts_per_page
    end_pos = start_pos + posts_per_page
    posts_of_present_page = posts[start_pos : end_pos]

    paginator = Paginator(posts, posts_per_page).page(page)
    has_next = paginator.has_next()
    has_previous = paginator.has_previous()
    nextpage = page
    previous_page = page
    if has_next:
        nextpage = paginator.next_page_number()
    if has_previous:
        previous_page = paginator.previous_page_number()

    custom_paginator = {
                               'posts' : posts_of_present_page,
                               'paginator' : paginator,
                               'has_next' : has_next,
                               'has_previous' : has_previous,
                               'nextpage' : nextpage,
                               'previous_page' : previous_page,
                       }
    return custom_paginator


@login_required
def linkboardpage(request, page=1):
#   Read & Access permission 
#   ( double validation for login, first : @login_required )
    try:
        reader = User.objects.get_user(request.user.id)
    except:
        messages.error(request, msg.linkboard_read_error)
        messages.info(request, msg.linkboard_anonymous_user_read) 
        return HttpResponseRedirect(reverse("users:login"))

    posts = LinkPost.objects.all().order_by('-date_posted')
    custom_paginator = pagination_of_linkboard(
                           posts=posts, 
                           posts_per_page = 10,
                           page=page
                       )

    return render(request, "linkboard/linkboardpage.html",
               {
                   'posts' : posts,
                   'paginator' :custom_paginator['paginator'],
                   'has_next' : custom_paginator['has_next'],
                   'has_previous' : custom_paginator['has_previous'],
                   'nextpage' : custom_paginator['nextpage'],
                   'previous_page' : custom_paginator['previous_page'],
               }
           )

                   

