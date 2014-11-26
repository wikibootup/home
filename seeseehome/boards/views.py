from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from boards.models import *
from seeseehome import msg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from django.core.urlresolvers import reverse

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

