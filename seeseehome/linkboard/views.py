from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request, Http404
from seeseehome import msg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from linkboard.models import LinkPost
from users.models import User
from boards.models import Board
from django.core.validators import URLValidator
from boards import views 

@login_required
def linkpost(request):
#   writer
    writer = request.user
#   does the writer have valid write permission?

    if not LinkPost.objects.is_valid_writeperm_to_linkpost(writer = writer):
        messages.error(request, msg.boards_write_error)
        messages.info(request, msg.boards_writer_perm_error)
        return HttpResponseRedirect(
                   reverse("linkboard:linkboardpage", args=(1,)))

    if request.method == 'POST':
#       url validator
        try:
            url = request.POST['url']
            urlvalidator = URLValidator()
            urlvalidator(url)
        except ValidationError:
            messages.error(request, msg.linkboard_linkpost_error)
            messages.info(request, msg.linkboard_linkpost_invalid)
            return HttpResponseRedirect(
                       reverse("linkboard:linkboardpage", args=(1,)))


        except UnicodeError:
            messages.error(request, msg.linkboard_linkpost_error)
            messages.info(request, msg.linkboard_linkpost_unicode_error)
            return HttpResponseRedirect(
                       reverse("linkboard:linkboardpage", args=(1,)))

#       description validator
        try:
            description = request.POST['description']
            LinkPost.objects.validate_description(description)
        except ValueError:
             messages.error(request, msg.linkboard_linkpost_error)
             messages.info(request, msg.boards_linkpost_description)
        except ValidationError:
             messages.error(request, msg.linkboard_linkpost_error)
             messages.info(
                request, 
                msg.boards_linkpost_description_at_most_255
             )
    
#       create link post
        LinkPost.objects.create_linkpost(
            writer = writer, 
            url = url, 
            description=description
        )
        return HttpResponseRedirect(
                  reverse("linkboard:linkboardpage", args=(1,)))
  
    boardlist = Board.objects.all()
    return render(request, "linkboard/linkpost.html", {'boardlist':boardlist})

@login_required
def linkboardpage(request, page=1):
    posts = LinkPost.objects.all().order_by('-date_posted')

#   if the page does not exist, raise 404
    try:
        custom_paginator = views.pagination(
                               posts=posts, 
                               posts_per_page = 10,
                               page=page
                           )
    except:
        raise Http404

    boardlist = Board.objects.all()

    return render(request, "linkboard/linkboardpage.html",
               {
                   'posts' : custom_paginator['posts'],
                   'paginator' :custom_paginator['paginator'],
                   'has_next' : custom_paginator['has_next'],
                   'has_previous' : custom_paginator['has_previous'],
                   'nextpage' : custom_paginator['nextpage'],
                   'previous_page' : custom_paginator['previous_page'],
                   'boardlist' : boardlist,
               }
           )

                   

