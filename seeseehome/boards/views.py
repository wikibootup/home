from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from boards.models import *
from seeseehome import msg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from django.core.urlresolvers import reverse
from boards.forms import WriteForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def write(request, board_id):
    form = WriteForm()
    if request.method == 'POST':
        is_valid_content = False

#       board
        board = Board.objects.get_board(board_id)

#       subject
        subject = request.POST['subject']
        try:
            Post.objects.validate_subject(subject)
        except ValueError:
            messages.error(request, msg.boards_write_error)
            messages.info(request, msg.boards_post_subject_must_be_set)
            return HttpResponseRedirect(reverse("boards:write"))
        except ValidationError:
            messages.error(request, msg.boards_write_error)
            messages.info(request, msg.boards_post_subject_at_most_255)
            return HttpResponseRedirect(reverse("boards:write"))

#       content
        if 'content' in request.POST:
            content = request.POST['content']
            try:
                Post.objects.validate_content(content)
            except ValidationError:
                messages.error(request, msg.boards_write_error)
                messages.info(request, msg.boards_post_content_at_most_65535)
                return HttpResponseRedirect(reverse("boards:write"))
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
        if Post.objects.is_valid_perm(
               boardperm = board.writeperm, 
               userperm = writer.userperm
           ):
            is_valid_writer = True
        else:
            messages.error(request, msg.boards_write_error)
            messages.info(request, msg.boards_writer_perm_error)
            return HttpResponseRedirect(reverse("boards:write"))

#       post save
        post = Post.objects.create_post(board=board, subject=subject, 
                writer=writer)

#       content save
        if is_valid_content:
            Post.objects.update_post(post.id, content=content)

        messages.success(request, msg.boards_write_success)
        messages.info(request, msg.boards_write_success_info)

        boardposts = BoardPosts.objects.filter(board=board)
        return render(request, "boards/boardpage.html", 
                {'board_id' : board_id, 'boardposts' : boardposts})

    return render(request, "boards/write.html", {'form' : form})

def postpage(request, board_id, post_id):
    board = Board.objects.get_board(board_id)
    post = Post.objects.get_post(post_id) 
    return render(request, "boards/postpage.html",
            {'board' : board, 'post' : post})

def boardpage(request, board_id):
    board = Board.objects.get_board(board_id)
    boardposts = BoardPosts.objects.filter(board=board)
    return render(request, "boards/boardpage.html", 
            {'board_id' : board_id, 'boardposts' : boardposts})

def boardlist(request):
    boardlist = Board.objects.all()
    return render(request, "boards/boardlist.html", {'boardlist' : boardlist})

