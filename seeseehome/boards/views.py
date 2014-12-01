from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from boards.models import *
from seeseehome import msg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from boards.forms import WriteForm
from django.core.paginator import Paginator

@login_required
def write(request, board_id, **extra_fields):
#   django-ckform not used. 
#   ckeditor widget class is used in template instead)
#   form = WriteForm()
    if request.method == 'POST':
        is_valid_content = False

#       does the writer have valid write permission?

#       board
        board = Board.objects.get_board(board_id)

#       subject
        subject = request.POST['subject']
        try:
            Post.objects.validate_subject(subject)
        except ValueError:
            messages.error(request, msg.boards_write_error)
            messages.info(request, msg.boards_post_subject_must_be_set)
            return HttpResponseRedirect(reverse("boards:write", 
                    args=(board_id)))
        except ValidationError:
            messages.error(request, msg.boards_write_error)
            messages.info(request, msg.boards_post_subject_at_most_255)
            return HttpResponseRedirect(reverse("boards:write",
                    args=(board_id)))

#       content
        if 'content' in request.POST:
            content = request.POST['content']
            try:
                Post.objects.validate_content(content)
            except ValidationError:
                messages.error(request, msg.boards_write_error)
                messages.info(request, msg.boards_post_content_at_most_65535)
                return HttpResponseRedirect(reverse("boards:write",
                        args=(board_id)))
            else:
                is_valid_content = True

#       writer
        try:
            writer = User.objects.get_user(request.user.id)
        except:
            messages.error(request, msg.boards_write_error)
            messages.info(request, msg.boards_anonymous_users_access) 
            return HttpResponseRedirect(reverse("users:login"))
 
#       write permission check
        if not Post.objects.is_valid_writeperm(
                board = board, writer = writer):
            messages.error(request, msg.boards_write_error)
            messages.info(request, msg.boards_writer_perm_error)
            return HttpResponseRedirect(reverse("boards:write",
                    args=(board_id)))

#       post save
#       If rewrite, no create, but update
        if not 'post_id' in extra_fields:
            post = Post.objects.create_post(board=board, subject=subject, 
                    writer=writer)
#       content save
            if is_valid_content:
                Post.objects.update_post(post.id, content=content)
        else:
            post_id = extra_fields['post_id']
            Post.objects.update_post(post_id, subject=subject)
            if is_valid_content:
                Post.objects.update_post(post_id, content=content)

        messages.success(request, msg.boards_write_success)
        messages.info(request, msg.boards_write_success_info)

        boardposts = \
            (BoardPosts.objects.filter(board=board)).order_by('-date_baord_posts_created')
        custom_paginator = pagination(
                               boardposts=boardposts, 
                               posts_per_page = 10
                           )
        return HttpResponseRedirect(reverse("boards:boardpage",
            args=(board_id, 1)))

    return render(request, "boards/write.html")

#@login_required
def rewrite(request, board_id, post_id):
    board = Board.objects.get_board(board_id)
    boardposts = BoardPosts.objects.filter(board=board)
    post = Post.objects.get_post(post_id) 
    
    if request.method == 'POST':
        write(request, board_id, post_id=post.id)
        boardposts = \
            (BoardPosts.objects.filter(board=board)).order_by('-date_baord_posts_created')
        custom_paginator = pagination(
                               boardposts=boardposts, 
                               posts_per_page = 10
                           )
        return HttpResponseRedirect(reverse("boards:boardpage",
            args=(board_id, 1)))

    return render(request, "boards/rewrite.html",
            {'board' : board, 'post' : post})

def postpage(request, board_id, post_id):
    board = Board.objects.get_board(board_id)
    post = Post.objects.get_post(post_id) 
    return render(request, "boards/postpage.html",
            {'board' : board, 'post' : post})

def pagination(boardposts, posts_per_page, page=1):
#   posts per page
    start_pos = (int(page)-1) * posts_per_page
    end_pos = start_pos + posts_per_page
    boardposts_per_page = boardposts[start_pos : end_pos]
    paginator = Paginator(boardposts, posts_per_page).page(page)
    has_next = paginator.has_next()
    has_previous = paginator.has_previous()
    nextpage = page
    previous_page = page
    if has_next:
        nextpage = paginator.next_page_number()
    if has_previous:
        previous_page = paginator.previous_page_number()

    custom_paginator = {
                               'boardposts' : boardposts_per_page,
                               'paginator' : paginator,
                               'has_next' : has_next,
                               'has_previous' : has_previous,
                               'nextpage' : nextpage,
                               'previous_page' : previous_page,
                           }
    return custom_paginator

def boardpage(request, board_id, page):
#   get board
    board = Board.objects.get_board(board_id)


#   the following line is important to the page list (prev page, next page)
    boardposts = \
        (BoardPosts.objects.filter(board=board)).order_by('-date_baord_posts_created')
    custom_paginator = pagination(boardposts=boardposts, posts_per_page = 10,
                        page=page)

    return render(request, "boards/boardpage.html", 
               {
                   'board_id' : board_id,
                   'boardposts' : custom_paginator['boardposts'],
                   'paginator' :custom_paginator['paginator'],
                   'has_next' : custom_paginator['has_next'],
                   'has_previous' : custom_paginator['has_previous'],
                   'nextpage' : custom_paginator['nextpage'],
                   'previous_page' : custom_paginator['previous_page'],
               }
           )

def boardlist(request):
    boardlist = Board.objects.all()
    return render(request, "boards/boardlist.html", {'boardlist' : boardlist})

